from pandas import DataFrame
import pandas as pd

DataFrame={'Nom':[],
           'Développeur':[],
           'Pays du développeur':[],
           'Année de publication':[],
           'Nombre de téléchargements':[],
           'Note appréciative':[],
           'Catégorie':[],
           'ESRB':[],
           'Publicité récompensées':[],
           'Publicité interstitielles':[],
           'Offerwall':[],
           'Microtransaction consumable':[],
           'Microtransacton non consummable':[],
           'Abonnement':[],
           'Montant minimum des micro-achats':[],
           'Montant maximum des micro-achats':[],
           'Tableaux de classement':[],
           'Notifications poussées':[]
           }



def export(application_list,file):
    #TODO: protect against different list length
    for count in range(0,len(application_list)):
        DataFrame['Nom'].append(application_list[count].name)
        DataFrame['Développeur'].append(application_list[count].developer)
        DataFrame['Pays du développeur'].append(application_list[count].developerCountry)
        DataFrame['Année de publication'].append(application_list[count].publicationYear)
        DataFrame['Nombre de téléchargements'].append(application_list[count].Downloads)
        DataFrame['Note appréciative'].append(application_list[count].Note)
        DataFrame['Catégorie'].append(application_list[count].category)
        DataFrame['ESRB'].append(application_list[count].ESRB)
        DataFrame['Publicité récompensées'].append(application_list[count].rewardedAds)
        DataFrame['Publicité interstitielles'].append(application_list[count].interstitialAds)
        DataFrame['Offerwall'].append(application_list[count].offerwall)
        DataFrame['Microtransaction consumable'].append(application_list[count].consummableIAP)
        DataFrame['Microtransacton non consummable'].append(application_list[count].permanentIAP)
        DataFrame['Abonnement'].append(application_list[count].subIAP)
        DataFrame['Montant minimum des micro-achats'].append(application_list[count].iap_minPrice)
        DataFrame['Montant maximum des micro-achats'].append(application_list[count].iap_maxPrice)
        DataFrame['Tableaux de classement'].append(application_list[count].leaderboard)
        DataFrame['Notifications poussées'].append(application_list[count].push_notification)
    df = pd.DataFrame(DataFrame)
    #file="./data_exported.xlsx"
    df.to_excel(file, index=False)



