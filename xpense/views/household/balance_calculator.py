import datetime
from collections import defaultdict
from typing import List, Optional, Dict

from xpense.database.repository_container import RepositoryContainer
from xpense.types import DataAggregation
from xpense.types import Transaction
from xpense.views.household.transaction_fetcher import TransactionFetcher

CONVERSION_FACTORS = {
    # From, to: factor
    (DataAggregation.WEEKLY, DataAggregation.MONTHLY): 4.33,
    (DataAggregation.WEEKLY, DataAggregation.YEARLY): 52,
    (DataAggregation.MONTHLY, DataAggregation.WEEKLY): 1 / 4.33,
    (DataAggregation.MONTHLY, DataAggregation.YEARLY): 12,
    (DataAggregation.YEARLY, DataAggregation.WEEKLY): 1 / 52,
    (DataAggregation.YEARLY, DataAggregation.MONTHLY): 1 / 12,
}


class BalanceCalculator:
    def __init__(self, repository_container: RepositoryContainer, current_datetime: datetime.datetime):
        self._transaction_fetcher = TransactionFetcher(repository_container, current_datetime)

    @staticmethod
    def _calculate_total(transactions: List[Transaction], aggregation: DataAggregation) -> float:
        total_amount = 0
        for transaction in transactions:
            amount = float(transaction.amount)
            key = (transaction.aggregation, aggregation)
            factor = CONVERSION_FACTORS.get(key, 1)
            total_amount += amount * factor
        return total_amount

    def get_total_expenses(self, aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY) -> float:
        expense_transactions = self._transaction_fetcher.get_expense_transactions(aggregation)
        return sum(float(t.amount) for t in expense_transactions)

    def get_total_income(self, aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY) -> float:
        income_transactions = self._transaction_fetcher.get_income_transactions()
        return self._calculate_total(income_transactions, aggregation)

    def get_total_allocations(self, aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY) -> float:
        allocation_transactions = self._transaction_fetcher.get_allocation_transactions()
        return self._calculate_total(allocation_transactions, aggregation)

    def get_total_unallocated_expenses(self, aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY) -> float:
        """
        Calculate unallocated expenses based on the following rules:
        - For each category:
            - If there is an allocation:
                - If allocation is negative, the absolute value is considered unallocated expense.
            - If there is no allocation, all expenses for that category are unallocated.
        """
        unallocated_expenses = 0.0
        allocations: List[Transaction] = self._transaction_fetcher.get_allocation_transactions()
        expenses: List[Transaction] = self._transaction_fetcher.get_expense_transactions(aggregation)

        # Sum allocations and expenses per category.
        allocation_per_category: Dict[str, float] = defaultdict(float)
        for alloc in allocations:
            key = (alloc.aggregation, aggregation)
            factor = CONVERSION_FACTORS.get(key, 1)
            allocation_per_category[alloc.category] += float(alloc.amount) * factor

        expense_per_category: Dict[str, float] = defaultdict(float)
        for exp in expenses:
            expense_per_category[exp.category] += float(exp.amount)

        # Set of all categories involved
        transaction_categories = set(allocation_per_category.keys()).union(set(expense_per_category.keys()))

        for category in transaction_categories:
            allocation = allocation_per_category.get(category, 0.0)
            expense = expense_per_category.get(category, 0.0)

            if allocation < expense:
                # Expenses exceed allocation; unallocated expense is the difference.
                unallocated_expenses += (expense - allocation)
            elif allocation == 0:
                # No allocation for this category; entire expense is unallocated.
                unallocated_expenses += expense

        return unallocated_expenses

    def get_total_balance(self, aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY):
        total_income = self.get_total_income()
        total_allocations = self.get_total_allocations()
        total_unallocated_expenses = self.get_total_unallocated_expenses(aggregation)
        return round(total_income - total_allocations - total_unallocated_expenses, 3)
