import os
from django.db import models
from django.db.models import Max
from web3 import Web3, HTTPProvider
from datetime import datetime

_STR_KWARGS = {'max_length': 200, 'null': True}


class BlockchainAddress(models.Model):
    address = models.CharField(primary_key=True, max_length=42, default="0x0")
    ens = models.CharField(**_STR_KWARGS)
    contract_name = models.CharField(**_STR_KWARGS)
    contract_abi = models.JSONField(default=dict, null=True)

    @property
    def etherscan_url(self):
        return "https://etherscan.io/address/" + self.address

    def appears_in(self):
        """ Return QuerySet of all transactions in which the address appears
        Uses related_names defined in BlockchainTransaction
        """

        txns = self.transactions_from.all()
        txns.union(self.transactions_to.all())
        txns.union(self.created_by_transaction.all())

        return txns

    def most_recent_appearance(self):
        """Return block number of most recent appearance in transactions
        
        If not found, return 0"""

        txns = self.appears_in()
        maxBlock = txns.aggregate(Max('block_number')).get('block_number__max')
        if maxBlock is None:
            maxBlock = 0 # May be None for two different reasons, so this catches both

        return maxBlock

    class Meta:
        db_table = "blockchain_addresses"

    def __str__(self):
        name = self.ens if self.ens is not None else self.address
        if self.contract_name is not None:
            name += f" ({self.contract_name})"
        return name


class BlockchainTransactionTrace(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default="0.0.0")
    from_address = models.ForeignKey(
        BlockchainAddress, 
        on_delete=models.CASCADE, 
        related_name="traces_from"
    )
    to_address = models.ForeignKey(
        BlockchainAddress, 
        on_delete=models.CASCADE,
        related_name="traces_to"
    )

    value = models.FloatField()
    error = models.CharField(max_length=20, null=True)
    compressed_trace = models.CharField(max_length=1000, null=True)
    output = models.CharField(max_length=1000, null=True)
    delegates = models.ForeignKey(
        BlockchainAddress, 
        on_delete=models.CASCADE,
        related_name="delegate_for_trace"
    )

    class Meta:
        db_table = "blockchain_traces"


class BlockchainTransaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=20, default="0.0")
    transaction_hash = models.CharField(max_length=66, null=True)
    block_number = models.PositiveIntegerField()
    from_address = models.ForeignKey(
        BlockchainAddress, 
        on_delete=models.CASCADE, 
        related_name="transactions_from"
    )
    to_address = models.ForeignKey(
        BlockchainAddress, 
        on_delete=models.CASCADE,
        related_name="transactions_to"
    )
    value = models.FloatField()
    error = models.CharField(max_length=20, null=True)
    articulated_trace = models.JSONField(default=dict, null=True)
    function_name = models.CharField(max_length=200, null=True)
    function_inputs = models.JSONField(default=dict, null=True)
    function_outpus = models.CharField(max_length=200, null=True) # List of values concatenated with spaces
    contracts_created = models.ManyToManyField(
        BlockchainAddress,
        related_name='created_by_transaction'
    )
    traces = models.ManyToManyField(
        BlockchainTransactionTrace,
        related_name='originating_from_transaction'
    )

    @property
    def timestamp(self):
        try:
            w3 = Web3(HTTPProvider(os.getenv('RPC_KEY')))
            timestamp_unix = w3.eth.get_block(self.block_number).timestamp
            timestamp = datetime.fromtimestamp(timestamp_unix)
        except Exception as e:
            print(e)
            timestamp = None
        return timestamp

    def contains_address(self, address):
        """Check if an address (string) appears anywhere in the transaction """

        addresFound = (
            self.to_address.address == address or
            self.from_address.address == address or
            address in [c.address for c in self.contracts_created]
        )

        return addresFound

    def is_internal(self):
        """Return true if any contracts were created, else false"""

        n_created = self.contracts_created.count()
        is_internal = True if n_created > 0 else False

        return is_internal

    class Meta:
        db_table = "blockchain_transactions"

    def __str__(self):
        return self.transaction_id


class DaoFramework(models.Model):
    name = models.CharField(max_length=200, default='not specified')
    website = models.URLField(**_STR_KWARGS)
    github = models.URLField(**_STR_KWARGS)

    class Meta:
        db_table = "dao_frameworks"
    
    def __str__(self):
        return self.name


class DaoFactory(models.Model):
    dao_framework = models.ForeignKey(
        DaoFramework, 
        on_delete=models.CASCADE,
        related_name='factories'
    )
    version = models.CharField(max_length=200, default='not specified')
    contract_address = models.OneToOneField(
        BlockchainAddress,
        on_delete=models.CASCADE
    )
    related_transactions = models.ManyToManyField(
        BlockchainTransaction,
        related_name='related_to_factory'
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "dao_factories"

    def __str__(self):
        return f"{self.dao_framework.name}, version {self.version}"


class EtlMonitor(models.Model):
    name = models.CharField(primary_key=True, max_length=20, default="test")
    last_scrape_time = models.DateTimeField(null=True)
    last_scrape_block = models.PositiveIntegerField(default=0) # TrueBlocks only

    class Meta:
        db_table = "etl_monitors"

    def __str__(self):
        return self.name