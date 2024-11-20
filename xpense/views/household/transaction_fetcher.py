import datetime
from typing import Optional, List

from dateutil.relativedelta import relativedelta

from xpense.database.repository_container import RepositoryContainer
from xpense.types import DataAggregation, Transaction, TransactionType


class TransactionFetcher:
    def __init__(self, repository_container: RepositoryContainer, current_datetime: datetime.datetime):
        self._rc = repository_container
        self._current_datetime = current_datetime

    def get_expense_transactions(
            self,
            aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY
    ) -> List[Transaction]:
        if aggregation == DataAggregation.WEEKLY:
            current_week_start = self._current_datetime - datetime.timedelta(days=self._current_datetime.weekday())
            current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            next_week_start = current_week_start + datetime.timedelta(weeks=1)
            expense_transactions: List[Transaction] = self._rc.transactions.get_by_conditions(
                conditions={
                    ("type", "=", TransactionType.EXPENSE),
                    ("date", '>=', current_week_start),
                    ("date", '<', next_week_start),
                },
                logic='AND'
            )

        elif aggregation == DataAggregation.YEARLY:
            current_year = self._current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            next_year = current_year + relativedelta(years=1)
            expense_transactions: List[Transaction] = self._rc.transactions.get_by_conditions(
                conditions={
                    ("type", "=", TransactionType.EXPENSE),
                    ("date", '>=', current_year),
                    ("date", '<', next_year),
                },
                logic='AND'
            )
        else:
            current_month = self._current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = current_month + relativedelta(months=1)
            expense_transactions: List[Transaction] = self._rc.transactions.get_by_conditions(
                conditions={
                    ("type", "=", TransactionType.EXPENSE),
                    ("date", '>=', current_month),
                    ("date", '<', next_month),
                },
                logic='AND'
            )
        return expense_transactions

    def get_income_transactions(self) -> List[Transaction]:
        # TODO: Add ending date for incomes because they may indeed have an end.
        income_transactions: List[Transaction] = self._rc.transactions.get_by_conditions(
            conditions={
                ("type", "=", TransactionType.INCOME),
                # ("end_date", '<=', current_month),
            },
            logic='AND'
        )
        return income_transactions

    def get_allocation_transactions(self) -> List[Transaction]:
        allocation_transactions: List[Transaction] = self._rc.transactions.get_by_conditions(
            conditions={
                ("type", "=", TransactionType.ALLOCATION),
                # ("end_date", '<=', current_month),
            },
            logic='AND'
        )
        return allocation_transactions

    def get_by_type(
            self, transaction_type: TransactionType,
            data_aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY
    ) -> List[Transaction]:
        if transaction_type == TransactionType.INCOME:
            return self.get_income_transactions()
        elif transaction_type == TransactionType.EXPENSE:
            return self.get_expense_transactions(aggregation=data_aggregation)
        else:
            return self.get_allocation_transactions()
