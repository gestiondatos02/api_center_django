from dataclasses import field
from pyexpat import model
from rest_framework import serializers 
from .models import Concepts, Contacts, Dates, Managements, AmountsMoney, SubConcepts, CompaniesCity, Branches, CompanyBranch, Reference, DescriptionBuget

class ConceptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepts
        fields = ['id', 'name']
        
class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name']
    
class DatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = ['id', 'date']
        
class ManagementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Managements
        fields = ['id', 'name']

class AmountsMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountsMoney
        fields = ['id', 'bs_amount', 'dolars_amount']
    
class SubConceptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubConcepts
        fields = ['id', 'sub_concept']
        
class CompaniesCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompaniesCity
        fields = ['id', 'name']
        
class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ['id', 'name']

class CompanyBranchSerializer(serializers.ModelSerializer):
    branch = BranchesSerializer(read_only=True)
    company = CompaniesCitySerializer(read_only=True)
    class Meta:
        model= CompanyBranch
        fields = ['id', 'branch', 'company']
        
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'name']
        
class DescriptionBugetSerializer(serializers.ModelSerializer):
    concept = ConceptsSerializer(read_only=True)
    sub_concept = SubConceptsSerializer(read_only=True)
    contact = ContactsSerializer(read_only=True)
    date = DatesSerializer(read_only=True)
    management = ManagementsSerializer(read_only=True)
    amount = AmountsMoneySerializer(read_only=True)
    companyBranch = CompanyBranchSerializer(read_only=True)
    reference = ReferenceSerializer(read_only=True)
    
    class Meta:
        model = DescriptionBuget
        fields = ['id', 'name', 'amount', 'companyBranch', 'concept', 'contact', 'date', 'management', 'reference', 'sub_concept'] 