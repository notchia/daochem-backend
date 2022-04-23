from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from daochem.database.models.blockchain import DaoFactory
from daochem.database.models.daos import Dao


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_factories = DaoFactory.objects.count()
    num_daos = Dao.objects.count()

    context = {
        'num_factories': num_factories,
        'num_daos': num_daos,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def factory_contract_summary(request, contract_address):
    fac = DaoFactory.objects.get(Q(contract_address=contract_address))
    r_lines = []
    r_lines.append(f"These are the results for the factory contract {fac.contract_address.contract_name} for {fac.dao_framework.name} version {fac.version} at {contract_address}")
    totalTransactions = fac.related_transactions.count()
    r_lines.append(f"Number of contract-creating transactions: {totalTransactions}")
    
    return HttpResponse("\n\n".join(r_lines))


def factories(request):
    context = {
        'factories': DaoFactory.objects.all()
    }

    return render(request, 'factories.html', context)


