from os import name
from turtle import mode
from django.db import models

class Concepts(models.Model):
    name = models.CharField(("Concepto"), max_length=50)
    
class Contacts(models.Model):
    name = models.CharField(("Contacto"), max_length=200)

class Dates(models.Model):
    date = models.CharField(("Fecha"), max_length=50)
    
class Managements(models.Model):
    name = models.CharField(("Gerencias"), max_length=200)

class AmountsMoney(models.Model):
    bs_amount = models.FloatField(null=True)
    dolars_amount = models.FloatField(null=True)

class SubConcepts(models.Model):
    sub_concept = models.CharField(("Sub concepto"), max_length=50)

class CompaniesCity(models.Model):
    name = models.CharField(("Empresa/Ciudad"), max_length=50)
    
class Branches(models.Model):
    name = models.CharField(("Sucursales"), max_length=50)

class CompanyBranch(models.Model):
    company = models.ForeignKey(("CompaniesCity"), on_delete=models.CASCADE)
    branch = models.ForeignKey(("Branches"), on_delete=models.CASCADE)

class Reference(models.Model):
    name = models.CharField(("Reference name"), max_length=50)

class DescriptionBuget(models.Model):
    name = models.CharField(("Descripcion"), max_length=50) 
    concept = models.ForeignKey("Concepts", on_delete=models.CASCADE)
    sub_concept = models.ForeignKey("SubConcepts", on_delete=models.CASCADE)
    contact = models.ForeignKey("Contacts", on_delete=models.CASCADE)
    date = models.ForeignKey("Dates", on_delete=models.CASCADE)
    management = models.ForeignKey("Managements", on_delete=models.CASCADE)
    amount = models.ForeignKey("AmountsMoney", on_delete=models.CASCADE)
    companyBranch = models.ForeignKey(("CompanyBranch"), on_delete=models.CASCADE)
    reference = models.ForeignKey(("Reference"), on_delete=models.CASCADE)
    