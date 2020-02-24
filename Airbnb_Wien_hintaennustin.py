#!/usr/bin/env python
# coding: utf-8

# # Airbnb-hintaennustin 
# 
# #### Johdatus datatieteeseen 2019 syksy,  harjoitustyö, Tapio Vaaranmaa (54338)
# 
# 

# ### 1. Kehitysympäristö
# 
# Hintaennustin tehtiin Python-koodilla Jupyter Notebooks -työkalun avulla. Myös dokumentaation kirjoitin suoraan Jupyter Notebook -tiedostoon Markdown-soluihin.  Kehitysympäristöksi asensin omaan kannettavaan tietokoneeseeni Jupyter Notebooksin sisältävän Anaconda-alustan (2019-10, Anaconda Navigator 1.9.7). Anaconda on erityisesti datatieteeseen ja koneoppiseen soveltuva ja runsaasti käytetty avoin Python- ja R-alusta, jota on helppo laajentaa Conda-paketinhallintatyökalulla. Anaconda Navigator on Anaconda-alustan graafinen käyttöliittymä, jolla voi luoda ja hallita erillisiä ympäristöjä sekä käynnistää valittuun ympäristöön asennettuja sovelluksia. Jupyter Notebook on selaimella käytettävä web-sovellus. Sitä käytetään aina selaimesta siitä riippumatta, onko sen palvelin paikallisella tietokoneella vai verkon takana.
# 
# Käyttöjärjestelmänä on Ubuntu 18.04 Linux, ja harjoitustyön julkaisualustana on [GitHub-repositorio](https://github.com/hip-pi/AirbnbVienna.git). Editorina käytin Visual Studio Codea ja vanhaa kunnon Emacsia, joskaan niitä ei juurikaan tarvinnut, sillä lähes kaiken sai kätevästi tehtyä suoraan Jupyter Notebookilla.  Asentamani Anaconda-distribuution Pythonin versio on 3.7.4 ja Jupyter Notebookin versio on 6.0.1. 
# 
# Asennuksessa tuli vähän sekoiltua, kun asensin ensin Pythonin uuden version suoraan ja sain koko käyttöjärjestelmän sekaisin määrittelemällä tämän uuden Python-tulkin oletustulkiksi: terminaaliohjelmakaan ei enää käynnistynyt. Tämä johtui siitä, että Linux-käyttöjärjestelmässä käynnistetään kaikenlaista Pythonin avulla ja tämä koodi on vanhempaa Pythonia, joten kaikki ei enää käynnistynyt käyttöjärjestelmässä kuten pitäisi. Tämä asennus oli kaiken lisäksi ihan turha, sillä Anacondan mukana tulee tarvittava Python-ympäristökin. Poistin tuhan asennuksen ja asensin Anacondan ohjeiden mukaisesti. Linuxiin asentaminen ei ole ihan niin suoraviivaista kuin Windowsiin, mutta netistä löytyneiden [ohjeiden](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-18-04) avulla se sujui kuitenkin kohtuullisen kivuttomasti.
# 
# Toinen varteenotettava vaihtoehto olisi ollut käyttää Jypyter Notebook -sovellusta CSC Notebooks -pilvipalvelun aikarajoitetutussa virtuaalikoneessa kuten koodiklinikalla tehtiin. Päädyin kuitenkin asentamaan tarvittavat ohjelmat omaan kannettavaan tietokoneeseeni, sillä sitä olisin kuitenkin käyttänyt, vaikka sovellusta olisikin ajettu verkon yli. Tämän vuoksi helpointa oli tehdä kaikki suoraan paikallisesti omalla koneella, ja näin ympäristökin jää minulle talteen.

# ### 2. Datan kerääminen ja tarkastelu
# Päätin käyttää  [Inside Airbnb](http://insideairbnb.com/) -datasettiä. Olisi ollut mielenkiintoisempaa tutkia jotain muuta data-aineistoa, mutta kurssi oli pakko jo saada pakettiin mahdollisimman pian ja siksi päätin valita tämän valmiin ja harjoituksista tutun datasetin. Tutkittavaksi kaupungiksi valitsin Wienin, sillä kaikki minulle tutummat kaupungit oli jo valittu tutkittavaksi. Minulle tutummista Budapestistä ja Etelä-Ranskan kaupungeista ei ollut data-aineistoa tässä datasetissä, enkä halunnut valita myöskään harjoituksissa käsiteltyä Berliiniä. Wien oli ainoa käsittelemätön kaupunki, josta minulla oli ennestään edes joku käsitys.
# 
# Inside Airbnb -datasetissä on Wienistä tallennettuna tiedostot listings.csv.gz, calendar.csv.gz, reviews.csv.gz, listings.csv, reviews.csv, neighbourhoods.csv ja neighbourhoods.geojson. Näistä ensimmäinen on mielenkiintoisin sisältäen yksityiskohtaista tietoa varauskohteista, toinen sisältää yksityiskohtaisen varauskalenterin ja kolmas kohteiden tekstimuotoisia arviointeja. Kaksi pakkaamatonta tiedostoa ovat vastaavien pakattujen tiedostojen yhteenvetoja ja viimeinen tiedosto sisältää tiedostossa neighbourhoods.csv lueteltujen kaupunginosien paikkatietoja. Dataa oli yli 10 tuhannesta kohteesta, joten sitä oli riittävästi, ja tiedot oli päivitetty viimeksi 19.11. 2019, joten data lienee ajantasaista ja luotettavaa.
# 
# Harjoitustyön pohjana käytin Nick Amaton blogia [Airbnb price predictor](https://mapr.com/blog/predicting-airbnb-listing-prices-scikit-learn-and-apache-spark/). Ihan ensimmäisenä otetaan käyttöön datan keräämiseen, jalostamiseen, kuvailemiseen sekä koneoppimisessa tarvittavia kirjastoja. Tutustuin aluksi tiedostojen tiedostot listings.csv.gz, calendar.csv.gz, reviews.csv.gz sisältöihin lukemalla ne Pandas-kirjaston dataframeiksi. Listings-dataframe sisälsi yhteensä 106 eri saraketta kohdeindeksi mukaan lukien. Reviews-dataframessa ainoa varsinainen tietosarake sisälsi tekstimuotoisia arvosteluja, joiden hyödyntäminen olisi ollut varsin vaikeaa tässä työssä. En myöskään kokenut tarpeelliseksi käyttää Calendar-dataframen tietoja hintaennustimessa, sillä sen sisältämät tulevaisuuden varaustiedot ja hintapyynnöt eivät tuntuneet ennusteen kannalta relevanteilta selittäjiltä. Tämän vuoksi päätin käyttää ennustimessa vain listings-tietoja ja pitäytyä alkuperäisen esimerkin sarakevalinnoissa, mutta karttavisualisointien vuoksi otin mukaan myös sarakkeet 'latitude' ja 'longitude' sekä kohteen Airbnb-linkin, jonka avulla valittua kohdetta voi tarkastella yksityiskohtaisesti. Lisäksi otin mukaan avainkentän ’id’ siltä varalta, että haluaisin kuitenkin myöhemmin hyödyntää calendar- tai reviews-tietoja. Otin talteen myös aineistossa olevan geojson-tiedoston wep-osoitteen, sillä käytän sitä karttavisualisoinneissa.
# 
# Halusin harjoitustyön lopuksi tehdä jonkinlaisen vuorovaikutteisen dashboardin Power BI -ohjelmistolla, mutta sen karttavisualisointi ei löytänyt kaikkia kaupunginosia pelkän nimen perusteella. Tämä johtunee kaupunginosien nimien sisältämistä umlaut- ja ß-merkeistä, jotka muutenkin aiheuttivat harmia pitkin harjoitustyötä. Wienissä käytetään yleisemmin kaupunginosanumeroita kuin niiden nimiä (esimerkiksi Innere Stadt on 1. Bezirke). Power BI -ohjelman karttavisualisointi löysikin kaupunginosat tämän kaupunginosanumeron perusteella. Tämän vuoksi lisäsin kaupunginosanumerot kohteet sisältävään dataframeen. Tein tämän raapimalla kaupunginosanumerot ja -nimet Wienin kaupungin web-sivuilta. Raavituista tiedoista muodostin ensin oman dataframen ja lopuksi yhdistin dataframet yhteen Pandaksen join-operaatiolla. Näin tuli kokeiltua oman datan keräämistäkin joskin varsin minimaalisella esimerkillä.

# In[ ]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import folium                              # conda install folium -c conda-forge
from folium.plugins import HeatMap 
from folium.plugins import MarkerCluster
import urllib
import json
from sklearn import impute
from sklearn import ensemble
from sklearn import linear_model
from sklearn.model_selection import learning_curve,GridSearchCV
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from collections import Counter


# In[ ]:


folder = 'http://data.insideairbnb.com/austria/vienna/vienna/2019-11-19/data/'
listings_file = folder + 'listings.csv.gz'
calendar_file = folder + 'calendar.csv.gz'
reviews_file  = folder + 'reviews.csv.gz'

folder = 'http://data.insideairbnb.com/austria/vienna/vienna/2019-11-19/visualisations/'
geojson_file  = folder + 'neighbourhoods.geojson'


# In[ ]:


df_c = pd.read_csv(calendar_file, compression='gzip')


# In[ ]:


df_c.head()


# In[ ]:


df_r = pd.read_csv(reviews_file, compression='gzip')


# In[ ]:


df_r.head(2)


# In[ ]:


df = pd.read_csv(listings_file, compression='gzip')


# In[ ]:


print(df.columns[0:50])   # tai print(pd.Series(df.columns).head(50))
print(df.columns[50:106])
len(df)


# In[ ]:


cols = ['id',
        'price',
        'accommodates',
        'bedrooms',
        'beds',
        'neighbourhood_cleansed',
        'room_type',
        'cancellation_policy',
        'instant_bookable',
        'reviews_per_month',
        'number_of_reviews',
        'availability_30',
        'review_scores_rating',
        'latitude',
        'longitude',
        'listing_url'
        ]

# read the file into a dataframe
df = pd.read_csv(listings_file, compression='gzip', encoding='utf-8', usecols=cols)


# In[ ]:


print(df.head())


# Tarkastellessani dataframen sisältöä, huomasin, että osa sarakkeen ’ neighbourhood_cleansed’ merkeistä jää tulostumatta oikein. Tämän ongelman selvittämiseksi ja korjaamiseksi piti tehdä vähän lisätarkasteluja.

# In[ ]:


df.neighbourhood_cleansed.unique()


# In[ ]:


df1 = pd.read_csv(listings_file, compression='gzip', encoding='utf-8', 
                  usecols=['neighbourhood'])
df1.neighbourhood.unique()


# Tarkasteltuani muiden sarakkeiden sisältöjä huomasin, että sarakkeen ’ neighbourhood_cleansed’ merkit on koodattu eri tavalla kuin muiden sarakkeiden merkit. Muualla koodaus oli utf-8, mutta sarakkeessa ’ neighbourhood_cleansed’ oli varsin epämääräinen koodaus. Koodaus vaikutti olevan muuten utf-8, mutta umlaut-merkien ja ß -merkin jälkimmäinen tavu näytti olevan mac_roman-koodauksen vastaava tavukoodi. Korjasin nämä virheelliset merkit metodin replace avulla, minkä jälkeen sarakkeen ’neighbourhood_cleansed’ näytti taas järkevältä ja kaupunginosien nimet tulostuivat siinä oikein.
# 
# Tämän asian ymmärtämiseen kului käsittämättömän paljon aikaa, sillä ensin luulin koko tiedoston merkkikoodauksen olevan joku erikoisempi, mutta mitään sopivaa ei löytynyt. Selitys löytyi vasta, kun aloin tutkia merkkijonojen tavusisältöä. Sitäkään tehdessä ei ensimmäisenä tule mieleen, että koodaus mennyt sekaisin, mutta mitään muuta selitystä en keksinyt. Muidenkin saksakielisten kaupunkien tiedostoja katselin enkä löytänyt niistä samaa ongelmaa.

# In[ ]:


df['neighbourhood_cleansed'] =     df['neighbourhood_cleansed'].replace(['\u008A','\u009A','\u009F','\u0080',
                                          '\u0085','\u0086','\u00A7'],
                                         ['ä','ö','ü','Ä','Ö','Ü','ß'], regex=True)
df.neighbourhood_cleansed.unique()


# Sitten raavitaan kaupunginosanumerot Wienin kaupungin web-sivuilta ja lisätään ne dataframeen, jotta voidaan lopuksi tehdä karttavisualisointi Power BI:lla.

# In[ ]:


response = requests.get('https://www.vienna.at/features/bezirke-wien') # read the web page
soup = BeautifulSoup(response.content, 'html.parser')

# Convert to string
pretty = soup.prettify()
#print(pretty)


# In[ ]:


bezirkes = soup.select('ul[id=bezirke] li', limit = 23)     # Soup object type, 
                                                            # total 23 bezirkes in Vienna
ordernumbers = []
names        = []
addresses    = []


# In[ ]:


# Go through all bezirkes in the list
for bezirke in bezirkes:
    # Get bezirke order number, name and address
    bezirkeData = bezirke.text.split('\n')
    ordernumbers.append(bezirkeData[1])
    names.append(bezirkeData[2])
    addresses.append(bezirkeData[3])
    
print(ordernumbers, names, addresses)


# In[ ]:


# Create a pandas dataframe
df_bezirkes = pd.DataFrame({'BezirkeNbr':ordernumbers, 'Bezirke':names, 'Zip':addresses})
df_bezirkes.head(23)


# In[ ]:


df_bezirkes.to_csv('bezirkes.csv', index=False, encoding='utf8') # save it (just for a case)


# Lopuksi yhdistetään raavitusta datasta muodostettu kaupunginosanumerot sisältävä dataframe kohteet sisältävään dataframeen.

# In[ ]:


# join this dataframe to the listing datafarame
df = df.join(df_bezirkes.set_index('Bezirke'), on = 'neighbourhood_cleansed') 


# In[ ]:


df.head(2)


# Talletetaan dataframe tiedostoon, jotta sen sisältöä voi halutessaan tarkastella myös muilla työkaluilla (esimerkiksi taulukkolaskentaohjelmalla).

# In[ ]:


df.to_csv('data.csv', index='False')

len(df.index)


# Kenttä ’ neighbourhood_cleansed’ sisältää kohteen kaupunginosan osan nimen. Kun tarkastellaan sen jakaumaa, havaitaan jakauman olevan Wienin datassa yllättävän tasainen: vain yhdessä kaupunginosassa on alle 100 kohdetta ja enimmillään kohteita on 1300. Kaupunginosia on yhteensä 23, joten kaupunginosajakokaan ei ole liian tarkka. Tämä kenttä vaikuttaa tässä aineistossa varsin käyttökelpoiselta, sillä eri kaupunginosista on varsin mukavasti rivejä. Esimerkissä käyytetty San Franciscon data oli paljon epätasaisemmin jakautunut.

# In[ ]:


nb_counts = Counter(df.neighbourhood_cleansed)
tdf = pd.DataFrame.from_dict(nb_counts, orient='index').sort_values(by=0)


# In[ ]:


# Redefining visualization width
plt.rcParams["figure.figsize"] = [20, 5]
tdf.plot(kind='bar')


# In[ ]:


len(nb_counts)


# In[ ]:


df_nb = pd.DataFrame.from_dict(nb_counts, orient='index', columns=['count'])
df_nb.columns


# In[ ]:


df_nb.sort_values(by=['count'], ascending=False).head(12)


# ### 3. Datan jalostaminen
# 
# Dataa tuli jalostettua jo edellisessä tarkasteluvaiheessa, kun korjasin kentän 'neighbourhood_cleansed' merkkijonokoodauksen. Kyseinen toimenpide oli kuitenkin lähinnä kosmeettinen; sen ainoa toiminnallinen merkitys liittyi siihen, että sitä käytettiin avainkenttänä yhdistettäessä kaksi datalähdettä. Tällaisia kosmeettisilta vaikuttavia jalostustoimenpiteitä ei kannata kuitenkaan aliarvioida, sillä datan esittäminen oikeassa muodossa on tärkeää ymmärrettävyydenkin vuoksi, kun dataa tutkitaan esimerkiksi visualisointien avulla. Tätä dataa täytyy toki hieman siivota ja jalostaa myös varsinaisista toiminnallisista syistä ennen kuin sitä kannattaa tarkemmin visualisoida ja ennen kuin sen avulla voi opettaa mallia. Puuttuvat arvot pitää imputoida tai puuttuvia arvoja sisältävät rivit pitää poistaa ja kategoriset (ei-numeeriset) arvot pitää korvata numeerisilla arvoilla.
# 
# Sarakkeessa 'reviews_per_month' on paljon puuttuvia arvoja. Tarkasteltaessa sarakkeiden 'number_of_reviews' ja 'reviews_per_month' arvoja havaitaan, että sarakkeessa 'reviews_per_month' on NaN-arvo ainoastaan silloin, kun sarakkeessa 'number_of_reviews' on nolla. Näin ollen sarakkeen 'reviews_per_month' NaN-arvot voidaan muuttaa nolliksi. Näin myös myöhemmin tehdään. Ensimmäinen alla olevista lausekkeista tarkistaa, ettei 'reviews_per_month' ole koskaan muuta kuin NaN silloin kun 'number_of_reviews' on nolla. Toinen lausekkeista tarkistaa, ettei 'reviews_per_month' ole koskaan NaN silloin kun 'number_of_reviews' poikkeaa nollasta. NaN-arvot ja arvioiden puuttuminen ovat siis ekvivalentit.

# In[ ]:


# the number of entries with 0 'number_of_reviews' which do not a NaN for 'reviews_per_month'
len(df[((df.number_of_reviews == 0) & (pd.isnull(df.number_of_reviews) == False)
       & (pd.isnull(df.reviews_per_month) == False))].index)


# In[ ]:


# the number of entries with at least 1 'number_of_reviews' which have a NaN for 'reviews_per_month'
len(df[(df.number_of_reviews != 0) & (pd.isnull(df.number_of_reviews) == False)
       & (pd.isnull(df.reviews_per_month) == True)].index)


# Korvataan kaikki NaN-arvot arvolla 0 sarakkeessa 'reviews_per_month', koska näistä kohteista ei ole arvioita. Lisäksi poistetaan aineistosta sellaiset epäilyttävät kohteet, joissa ei ole makuuhuoneita (0 sarakkeessa 'bedrooms') tai vuoteita (0 sarakkeessa 'beds'). Myöhemmin poistetaan myös kohteet, joiden hinta on 0, mutta hintasarakkeesta pitää poistaa <span>&#36;</span>-merkki ja se pitää muuttaa numeeriseksi ennen kuin 0-hintaiset kohteet kannattaa poistaa. <b>Alkuperäisessä esimerkissä tämä hintasuodatus tehty väärin jo tässä kohdassa ilman $-merkkiä, eikä se siten poista 0-hintaisia kohteita.</b> Lopuksi poistetaan vielä aineistosta kaikki kohteet, joihin on jäänyt NaN-arvo johonkin sarakkeeseen. Kaikkia kohteita ei olisi välttämätöntä poistaa, vaan voitaisiin myös yrittää imputoida puuttuvia arvoja muiden kohteiden arvojen avulla. Esimerkiksi sarakkeen 'review_scores_rating' NaN-avot voitaisiin imputoida vaikkapa sen muista kohteista laketulla keskiarvolla. Näin saataisiin muiden sarakkeiden suurempi aineisto ennustusmallinopetukseen, mutta visalisointiin tulisi näkyviin tekaistuja arviointintilukemia, mikä ei ole suotavaa.

# In[ ]:


# so we need to do some cleaning.

# first fixup 'reviews_per_month' where there are no reviews
df['reviews_per_month'].fillna(0, inplace=True)

# just drop rows with bad/weird values
# (we could do more here)
df = df[df.bedrooms != 0]
df = df[df.beds != 0]
#df = df[df.price != 0]    # TÄTÄ EI VOI TEHDÄ VIELÄ TÄSSÄ, sillä ensin on poistettava $-merkit

# 'review_score_rating' NaN-arvot voisi myös imputoida esimerkiksi näin:
imputer = impute.SimpleImputer(strategy='median')  
#df.review_scores_rating = imputer.fit_transform(df.review_scores_rating.values.reshape(-1, 1)).reshape(-1, 1)

df = df.dropna(axis=0)  # poistetaan kuitenkin kaikki rivivit, joissa on jäljellä NaN-arvoja
                        # tarkastellaan kaikkia asuntoja toisin kuin alkuperäisessä esimerkissä 
len(df.index)


# In[ ]:


df.price.head(5)


# In[ ]:


# remove the $ from the price and convert to float
df['price'] = df['price'].replace('[\$,)]','',          regex=True).replace('[(]','-', regex=True).astype(float)
df.price.sort_values(ascending=False).head(61)


# In[ ]:


df.price.sort_values(ascending=True).head(100)


# Nyt $-merkit on poistettu hintakentästä ja se on muutettu liukuluvuksi, joten dataframesta voidaan poistaa ne rivit, joista hinta puuttuu. Näitä tosin ei näytä olevan tässä aineistossa. Aineistossa näyttää olevan 60 kohdetta, joiden hinta on yli 500. Poistetaan nämä kalliit asunnot dataframesta, koska nämä eivät kiinnostane normaalia asunnon vuokraajaa ja jotta jakaumista saadaan tehtyä informatiivisempia kuvia. Tarkastellaan kuitenkin ensin, missä kalliit asunnot sijaitsevat. Alla olevasta listauksesta nähdään, että kalliita asuntoja on yllättäen ympäri kaupunkia, joskin ne painottuvat eskusta-alueelle. Niiden merkitys on kuitenkin varsin vähäinen analysoitaessa kaupunginosien hintatasoja.

# In[ ]:


df[df.price > 500].groupby(
     ['neighbourhood_cleansed']
  ).agg(
    count=('id', len)
).sort_values(by=['count'], ascending=False)


# In[ ]:


# Nyt voi tehdä hintaan perustuvat suodatukset
df = df[df.price != 0] # turha Wien-aineistossa 19.11.2019
df = df[df.price <= 500]
len(df)


# In[ ]:


# Talletetaan siivottu data PowerBI:ta varten visualisoitavaksi
df.to_csv('data_windows.csv', encoding='windows-1252')


# Osa mukaan valituista piirteistä on kategorisia, joten niiden avulla ei voi suoraan opettaa ennustemallia. Joukossa on myös pelkästään visualisointia varten mukaan otettuja muuttujia, jota voidaan tiputtaa pois dataframesta ennen opettamista. Tällaisia ovat esimerkiksi kohteen url sekä kaupunginosanumero ja postiosoite.
# 
# Selittäjiksi suunnitellut kategoriset piirteet pitää kuitenkin muuttaa numeerisiksi. Merkkijonomuotoisen kentän 'neighborhood_cleansed' tietosisältö saadaan muutettua numeeriseksi ns. dummy-muuttujien avulla käyttämällä Pandaksen funktiota get_dummies. Menetelmää kutsutaan nimellä "one hot encoding". Siinä jokaista sarakkeen merkkijonoarvoa kohden muodostetaan uusi sarake. Kunkin rivin merkkijonoa vastaavaan uutteen sarakkeeseen sijoitetaan arvo 1 ja kaikkiin muihin uusiin muodostettuihin sarakkeisiin sijoitetaan arvo 0. Samaa menetelmää käytetään myös merkkijonomuotoisille kentille 'room_type' ja 'cancellation_policy'.
# 
# Kenttä 'instant_bookable' on myös muodollisesti merkkijono, mutta sillä on vain kaksi arvoa 't' ja 'f', joten tosiasiallisesti se kuvaa totuusarvoa. Siitä generoidaan myös ensin uudet sarakkeet samalla menetelmällä, mutta muodostuviin lisätään prefix 'instant'. Koska muodostuvat kaksi saraketta ovat toistensa vastakohdat, poistetaan lopuksi arvoja epätosi edustava sarake. Kaikki funktiolla get_dummies muodostetut sarakkeet pitää lopuksi lisätä piirteet sisältävään dataframeen (alldata), ja niitä vastaavat kategoristen muuttujien sarakkeet pitää vastaavasti tiputtaa pois dataframesta.

# In[ ]:


# get feature encoding for categorical variables
n_dummies = pd.get_dummies(df.neighbourhood_cleansed)
rt_dummies = pd.get_dummies(df.room_type)
xcl_dummies = pd.get_dummies(df.cancellation_policy)

# convert boolean column to a single boolean value indicating whether this listing has instant booking available
ib_dummies = pd.get_dummies(df.instant_bookable, prefix="instant")
ib_dummies = ib_dummies.drop('instant_f', axis=1)

# replace the old columns with our new one-hot encoded ones
alldata = pd.concat((df.drop(['neighbourhood_cleansed',     'room_type', 'cancellation_policy', 'instant_bookable'], axis=1),     n_dummies.astype(int), rt_dummies.astype(int),     xcl_dummies.astype(int), ib_dummies.astype(int)),     axis=1)
allcols = alldata.columns
alldata.head(5)


# ### 4. Datan kuvaileminen
# 
# Ensimmäiseksi kuvailin asuntojen hintoja alueittain boxplot-kaavion avulla. Kaavion luettavuuden vuoksi siihen ei voi ottaa mukaan kaikkia 23 kaupunginosaa. Ei myöskään ole mielekästä tarkastella samalla asteikolla 50 ja yli 500 kohteen kaupunginosia. Kaaviota varten muodostetaan ensin indeksitaulukko 'top_neighbourhoods', johon otetaan mukaan ne kaupunginosat, joissa on alkuperäisessä aineistossa yli 500 vuokrauskohdetta. Indeksitaulukko lajitellaan, ja sen avulla poimitaan siivotusta (kategoriset muuttujat sisältävästä) dataframesta näiden suositumpien kaupunginosien kohteet dataframeen 'df_top'. Tästä dataframesta piirretään boxplot-kaavio kaupunginosien hintatasosta kirjaston Seaborn funktiolla boxplot. Kaaviosta nähdään, että vuokrauskohteiden hinnat ovat jakautuneet varsin samalla tavalla kaikissa muissa paitsi 1. kaupunginosassa Innere Stadt, eli vain aivan ydinkeskustan kohteet ovat selvästi muita kalliimpia. 
# 

# In[ ]:


# Some kind of a boxplot 
df.price.value_counts()
top_neighbourhoods= df_nb[df_nb['count'] > 500].sort_values(by=['count'],ascending=False).index
df_top = df[df.neighbourhood_cleansed.isin(top_neighbourhoods)]
df_top.head()


# In[ ]:


import seaborn as sns
AX = sns.boxplot(x='neighbourhood_cleansed', y='price', data=df_top)


# Seuraavaksi oli karttavisualisointien vuoro, sillä asuntokohteiden tarkastelussa asunnon sijainti ja sen ympäristö kiinnostavat yleensä erittäin paljon vuokraajaa. Päätin käyttää näihin visualisointeihin Teppo Kivennon löytämää kirjastoa Folium. Kirjastoa ei ollut valmiiksi Anacondassa, joten asensin sen oheistuksen mukaisesti (conda install folium -c conda-forge). Netistä löytyi aika paljon esimerkkejä tämän kirjaston käyttämisestä (esimerkiksi [Quickstart](https://python-visualization.github.io/folium/quickstart.html), [kaggle](https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-data) ja [Medium](https://medium.com/@bobhaffner/folium-markerclusters-and-fastmarkerclusters-1e03b01cb7b1)). Toteutin Folium-kirjaston avulla kohteiden lämpökartan, kohdekartan ja kaupunginosakartan. Kohdekartassa käytetään kohdeklusterointia ryhmittelemään yksittäisiä kohteita eri zoomaustasoilla. Klusterointi muuttuu automattisesti zoomatessa.
# 
# Lämpökartta antaa aika karkean kuvan kohteista, mutta zoomaamalla siitäkin saa jotain informaatiota. Lämpökartta talletetaan tiedostoon [heat_map.html](https://tuni-my.sharepoint.com/:u:/g/personal/tapio_vaaranmaa_tuni_fi/EUHphGqtNedLlpXlOOkSNGsBf9aKaF9_NSj0psoiTPOjoQ?e=ibvJJx). Klusteroidun kohdekartan avulla on helpompi hahmottaa kohteiden sijaiti ja niitä pääsee myös tarkastelemaan. Liitin kohteisiin popup-tulosteet, jotka sisältävät kohteen hinnan, majoituskapasiteetin ja Airbnb-linkin. Kun linkkiä klikkaa popupista, avautuu kohteen Airbnb-sivu uuteen selaimen välilehteen. Chrome ei tulostanut kuvaa Jupyterissa, jos siinä on yli 2000 popup-tulostetta, mutta talletetusta html-tiedostosta ([listing_map.html](https://tuni-my.sharepoint.com/:u:/g/personal/tapio_vaaranmaa_tuni_fi/ESrBDKw_VIRPkJwLDszE_m0Bu1gWF-gmVFhF0fiyTiT3JQ?e=KRo1Dq)) se generoi kuvan erilliseen ikkunaan. Firefoxissa kuva tulostui myös Jupyter Notebookissa, vaikka kaikkiin kohteisiin liittyi popup. Tämän seurauksena siirryin käyttämään Firefoxia Jupyter Notebookin kanssa.
# 
# Kohdekartan lisäksi tein foliumilla myös karttavisualisoinnin kaupunginosista Inside Airbnb -datasetin sisältämän geojson-datan avulla. Valitettavasti tässäkin tiedostossa oli taas kaupunginosien nimissä sama kummallinen merkkikoodaus, ja jouduin taas konvertoimaan merkkijonot. Määritin kaupunginosille eri värit, jotta ne erottuvat selkeästi kartassa. Lisäsin karttaan jokaisen kaupunginosan kohdalle kohteiden yhteenvetotietoja sisältävän popup-tulosteen. Popup-tuloste sisältää kohteiden keskihinnan, arvioiden keskiarvon sekä kohteiden lukumäärän yhteensä ja kohdetyypeittäin. Tämän kartan avulla saa yleiskatsauksen kohteiden hintatasosta ja lukumääristä eri puolilla Wieniä ja voi tarkastella kaupunginosien välisiä eroja. Tallensin tämän kartan tiedostoon [bezirke_map.html](https://tuni-my.sharepoint.com/:u:/g/personal/tapio_vaaranmaa_tuni_fi/EWkaZjDmv9NOs0IePiJCkY8BaYJD7RUaVpz1XZJ9fsq75Q?e=SfG60q).
# 
# Tarkastelin myös Wienin kaupungin avointa dataa ja totesin, että tarjolla oli runsaasti erilaisia paikkatietoja sisältäviä datalähteitä. Koska Wienissä on valtavasti erilaisia museoita, päätin kokeilla lisätä kaupunginosakarttaan löytämäni museolistauksen kohteet. Generoin tämän kartan uusteen ikkunaan, sillä merkintöjä oli niin paljon, ettei keskikaupungin kaupunginosiin pystynyt enää kohdistamaan osumatta museomerkintään, jollei zoomannut lähemmäksi. Museoista kiinnostunut asunnon vuokraaja voi valita asunnoin kaupunginosan tämän kartan avulla. Tämä kartta löytyy talletettuna tiedostosta [museum_map.html](https://tuni-my.sharepoint.com/:u:/g/personal/tapio_vaaranmaa_tuni_fi/EdZoFBW6luNOq_jbKKK6TDUBpDtykF5olwVDR12lPQNcVg?e=4qatE5). Kartat tulostuvat Jupyter Notebooksissa vain sillä istuntokerralla, jolla ne generoidaan. Ne eivät näy myöskään GitHubissa avattaessa Jupyter Notebook -tiedosto. Edellä mainituista tiedostoista kartat ovat suoraan ladattavissa selaimeen, ja karttatiedostot ovat myös ladattavissa GitHubista. Suosittelen käyttämään Firefoxia.

# In[ ]:


map = folium.Map(location=[48.210033, 16.363449], zoom_start = 12)
#folium.TileLayer("OpenStreetMap").add_to(map)

coordinates = np.array([alldata.latitude.to_list(), alldata.longitude.to_list()]).T 
                                                                 # transpose matrix
HeatMap(coordinates).add_to(map)
map.save('heat_map.html')
map


# In[ ]:


map = folium.Map(location=[48.210033, 16.363449], zoom_start = 12)

marker_cluster_group = MarkerCluster(name="Airbnb").add_to(map)

for row in alldata.iterrows():
    text = ('Price: ' + str(row[1].price) + '<br>' +
            'Accommodates: ' + str(row[1].accommodates) + '<br>' + 
            '<a href =\"' + str(row[1].listing_url) + '\" target=\"_blank\">' + 
                            str(row[1].listing_url) + '</a></p>'
           )
    folium.Marker(location=[row[1].latitude, row[1].longitude],
                  popup = folium.Popup(text, max_width=250)).add_to(marker_cluster_group)

marker_cluster_group.add_to(map)
map.save('listing_map.html')
map


# In[ ]:


map = folium.Map(location=[48.210033, 16.363449], zoom_start = 11)
folium.TileLayer('stamenterrain').add_to(map) # kokeillaan maastomuotokarttaa

fp = urllib.request.urlopen(geojson_file) # noudetaan geojson-tiedosto suoraan netistä
geodata = json.load(fp)

bezirkeFillColors = ['#0000ff','#00ff00','#ff0000','#00ffff','#ffff00','#ff00ff',
                     '#7700ff','#77ff00','#770000','#77ffff','#77ff00',
                     '#0077ff','#007700','#ff7700','#0077ff','#ff7700',
                     '#000077','#00ff77','#ff7700','#00ff77','#ffff77',
                     '#ff7777','#000000']
i = 0 # väri-indeksi

for feature in geodata['features']:
    geo_n = folium.GeoJson(
        feature,
        style_function = lambda x, fillColor = bezirkeFillColors[i]: {
            'fillColor': fillColor,
            'color': 'black'
        }
    )
    bezirke = feature['properties']['neighbourhood'] 
    # Kummallisen koodauksen vuoksi pitää taas muuttaa merkkejä:
    bezirke = bezirke.translate(bezirke.maketrans('\u008A\u009A\u009F\u0080\u0085\u0086\u00A7',
                                                  'äöüÄÖÜß'))
    bezdata = alldata[alldata[bezirke] == 1] # haetaan rivit, joiden kaupunginosasarakkeessa 1
    text = (
        '<h5><b>' + bezirke + '</b></h5>' +
        'Average Price: ' + str(round(bezdata.price.mean(),2)) + '<br>' +
        'Average Rating: ' + str(round(bezdata.review_scores_rating.mean())) + ' (of 100)<br>'+
        'Apartments: ' + str(len(bezdata)) + '<br>' +
        '<ul><li>entire apartment: ' + 
                               str(len(bezdata[bezdata['Entire home/apt'] == 1])) + '</li>' +
        '<li>private room: ' + str(len(bezdata[bezdata['Private room'] == 1])) + '</li>' +
        '<li>shared room: ' + str(len(bezdata[bezdata['Shared room'] == 1])) + '</li>' +
        '<li>hotel room: ' + str(len(bezdata[bezdata['Hotel room'] == 1])) + '</li></ul>'
    )
    geo_n.add_child(folium.Popup(text, max_width=250))
    geo_n.add_to(map)   
    i = i + 1

map.save('bezirke_map.html')
map


# In[ ]:


fp = urllib.request.urlopen('https://data.wien.gv.at/daten/geo?service=WFS&request=' + 
                            'GetFeature&version=1.1.0&typeName=ogdwien:MUSEUMOGD&srsName=' +
                            'EPSG:4326&outputFormat=json')
museumdata = json.load(fp)
folium.TileLayer('OpenStreetMap').add_to(map)

for museum in museumdata['features']:
    folium.Marker(location=[museum['geometry']['coordinates'][1], 
                            museum['geometry']['coordinates'][0]],
                  popup=folium.Popup(museum['properties']['NAME'], max_width=150),
                  icon = folium.Icon(color='red', icon='home')).add_to(map)
    

map.save('museum_map.html')
map


# Seuraavaksi tarkastelin eri piirteiden välisiä korrelaatioita. Pandaksen avulla saa piirrettyä lämpöväritetyn korrelaatiomatriisin, joka on varsin informatiivinen ja josta helposti löytää vahvimmat positiiviset ja negatiiviset korrelaatiot. Matriisi on varsin laaja, mutta erityisesti silmään pistää varsin vahva negatiivinen korrelaatio kohdetyyppien "Private room" ja "Entire home/apt" välillä, mikä käytännössä tarkoittaa kyseisten muuttujien olevan toistensa vastakohdat. Koska nämä muuttujat käytännössä suoraan määräävät toistensa arvot, niin vain toista niistä voi käyttää selittäjänä; lienee aika lailla yhdentekevää, kumpi otetaan selittäjäksi. Majoituskapasiteetilla sekä makuuhuoneiden ja sänkyjen lukumäärällä näyttää myös olevan sen verran vahva positiivinen korrelaatio, että varsinkin niistä kannattaa piirtää hajontapistekaaviot tarkempaa tarkastelua varten.

# In[ ]:


# Lämpöväritetty korrelaatiomatriisi
corr = alldata.corr(method='pearson')
corr.style.background_gradient(cmap='coolwarm').set_precision(3)


# Tarkastelin vielä tarkemmin piirteiden korrelointia hinnan kanssa saadakseni perusteita hinnan ennustemallille. Poimin kaikki itseisarvoltaan 0.1 suuremmat korrelaatiot hinnan kanssa ja tulostin ne suuruusjärjestyksessä. Joukosta erottui muutama selvästi nollasta poikkeava korrelaatio. Selvästi suurin negatiivoinen korrelaatio on piirteen 'Private room' kanssa ja selvimmät positiiviset korrelaatiot ovat piirteiden 'accommodates', 'bedrooms', 'beds', 'Entire home/apt', 'Innere Stadt' ja 'availability_30' kanssa, joista 'Entire home/apt' kuvaa selvästi samaa asiaa kuin 'Private room' mutta vastakkaiseen suuntaan. Kaupunginosista ainoastaan Innere Stadt näyttäisi selvästi vaikuttavan hintaan, mikä on tullut esiin jo aiemmissakin tarkasteluissa.

# In[ ]:


corr.price.sort_values(ascending=False)[abs(corr.price) > 0.1]


# Pandaksen funktiolla scatter_matrix puolestaan saadaan tehtyä hajontapistematriisi, jonka avulla voi tarkastella piirteiden välisiä keskinäisiä riippuvuuksia. Voidaan esimerkiksi tarkastella, esiintyykö piirteiden välillä kollineaarisuutta tai selittävillä piirteillä heteroskedastisuutta ([KvantiMOTV/Regressioanalyysin rajoitteet](https://www.fsd.tuni.fi/menetelmaopetus/regressio/rajoitteet.html)). Lävistäjämatriisilla näkyy puolestaan kunkin piirteen arvoalue histogrammeina. Selittävien piirteiden välinen kollineaarisuus vaikuttaisi negatiivisesti regressiomallin tuloksiin, ja todennäköisesti se ilmenisi hajantapistematriisiin muodostuvina suorina.
# 
# Alla olevasta hajontapistematriisista nähdään, ettei kollineaarisuuden suhteen esiinny selviä ongelmia valitussa selittäjäjoukossa. Sänkyjen sekä makuuhuoneiden lukumäärän ja majoituskapasiteetin välillä on luonnollisesti jonkin asteinen riippuvuus, mutta niidenkään välinen pistejoukko ei muodosta selvää suoraa, joten riippuvuus ei ole liian vahva. Erilaiset majoitusratkaisut eri huoneistoissa vaikuttavanet siihen, ettei suoraa riippuvuutta ole. 
# 
# Heteroskedastisuus näkyisi hajontapistematriisissa selitettävän (hinta) ja selittävien muuttujien (muut) hajontakuvioissa suorina, joissa virhetermin arvo vaihtelisi suuresti selittäjän arvon mukaan. Heteroskedastisuus ei estä piirteen käyttämistä selittäjänä, mutta vaikuttaa siihen, mitä menetelmää kannattaa käyttää. Sitäkään ei ole selvästi havaittavissa valituissa piirteissä. Tosin millään matriisin selittävillä piirteellä ja hinnalla ei näyttäsi olevan myöskään selvää lineaarista riippuvuutta.

# In[ ]:


scattercols = ['price', 'accommodates', 'number_of_reviews', 'reviews_per_month',
               'beds', 'bedrooms', 'availability_30', 'review_scores_rating']
axs = pd.plotting.scatter_matrix(alldata[scattercols], figsize=(15, 15), c='red')


# ### 5. Koneoppiminen
# 
# Nyt kun data on jalostettu sopivaan muotoon ja sen sisältöä ymmärretään riittävästi, voidaan luoda asunnon hinnan ennustemalli tai -malleja. Kokeillaan ensin käyttää hinnan ennustamiseen alkuperäisen esimerkin piirrejoukkoa. Kirjaston scikit-learn avulla on helppo kokeilla useita erilaisia lineaarisia ennustemalleja samalla datalla. Kokeillaan aluksi kuutta eri mallia: pienimmän neliösumman lineaarinen regressio, Ridge-regressio, Lasso-regressio, ElasticNet-regressio, Bayesian-regressio ja Orthogonal Matching Pursuit (OMP). (https://scikit-learn.org/stable/modules/linear_model.html)
# 
# Vertaillaan mallien hyvyyttä käyttäen mittarina virhetermien itseisarvon mediaania. Virheiden mediaani on esimerkiksi keskimääräistä neliövirhettä parempi mittari, koska outlierit vaikuttavat siihen kohtuullisen vähän. Selkeimmät outlierit toki suodatin jo pois dataa siivotessani, mutta aineistoon jäi kuitenkin merkittävästi keskiarvoa ja mediaania suurempia arvoja. Virheiden mediaani on hyvä mittari myös siksi että sen yksikkö on sama testattavan suureen (tässä hinnan) kanssa ja arvot ovat siten helposti ymmärrettäviä. 
# 
# Piirrematriisista poistetaan ennustettava piirre (hinta) sekä siihen visualisointien vuoksi lisätyt piirteet, joita ei ollut tarkoituskaan käyttää ennustamisessa. Tämän jälkeen piirrematriisi ja niitä vastaavat hinnat jaetaan kahteen osaan funktiolla train_test_split. Testiä varten valitaan arvoista 20% satunnaisesti. Kaikki mallit opetetaan niiden metodeilla fit ja tämän jälkeen niiden testiaineistosta muodostamat ennusteet (funktion predict palauttama vektori) testataan testiaineiston todellisia hintoja vastaan ja virhe tulostetaan. Lopuksi piirretään eri mallien virheistä pylväsdiagrammit. Kaikki mallit tuottavat suunnilleen samansuuruisen virheen (virhealue on 17.01 - 18.88); vain ElasticNet-mallin virheen voi katsoa olevan vähän muita suurempi. Tulosten perusteella valitsisin perinteisen pienimmän neliösumman regression, koska ymmärrän malleista kunnolla vain sen toiminnan ja sen virhe on vain puoli prosenttia pienintä virhettä suurempi. Mitään todellista hyvyyseroa ei siis ole. Katsotaan lopuksi, miltä ennustukset näyttävät suhteessa todellisiin arvoihin näillä menetelmällä. Suhteelliset poikkeamat ovat kohtuullisen suuria eikä ennustin vaikuta kovin käyttökelpoiselta.

# In[ ]:


rs = 1
ests = [ linear_model.LinearRegression(), linear_model.Ridge(),
         linear_model.Lasso(), linear_model.ElasticNet(),
         linear_model.BayesianRidge(), linear_model.OrthogonalMatchingPursuit() ]
ests_labels = np.array(['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'BayesRidge', 'OMP'])
errvals = np.array([])

X_train, X_test, y_train, y_test =     train_test_split(alldata.drop(['price', 'id', 'listing_url', 'longitude', 'latitude', 
                                   'BezirkeNbr', 'Zip'], axis=1),
                     alldata.price, test_size=0.2, random_state=20)

for e in ests:
    e.fit(X_train, y_train)
    this_err = metrics.median_absolute_error(y_test, e.predict(X_test))
    print("got error %0.2f" % this_err)
    errvals = np.append(errvals, this_err)

pos = np.arange(errvals.shape[0])
srt = np.argsort(errvals)
plt.figure(figsize=(7,5))
plt.bar(pos, errvals[srt], align='center')
plt.xticks(pos, ests_labels[srt])
plt.xlabel('Estimator')
plt.ylabel('Median Absolute Error')


# In[ ]:


pd.DataFrame({'Price' : y_test, ests_labels[0] : ests[0].predict(X_test),
                                ests_labels[1] : ests[1].predict(X_test),
                                ests_labels[2] : ests[2].predict(X_test),
                                ests_labels[3] : ests[3].predict(X_test),
                                ests_labels[4] : ests[4].predict(X_test),              
                                ests_labels[5] : ests[5].predict(X_test),
             })


# Seuraavaksi kokeillaan hyperparametrien optimointia (hyperparameter tunining) ja katsotaan, saadaanko sen avulla parempi tulos. Hyperparametreilla tarkoitetaan sellaisia mallin parametreja, joiden arvo ei muutu koneoppimisen opetusprosessin aikana. Hyperparametrien optimointi löytää hyperparametrien joukon, joka tuottaa optimaalisen mallin ja joka minimoi ennalta määritellyn häviöfunktion käytetyllä syötedatalla. Yleinen optimoinnissa käytettyy menetelmä on grid search, joka kokeilee kaikkia valittujen parametrien arvokombinaatioita ja käyttää ristiinvalidointia löytääkseen parhaan kombinaation. Kirjaston sklearn funktiolla GridSearchCV voidaan tehdä grid search valitun menetelmän valituille parametreille.
# 
# Valitaan optimoitavaksi ennustusmenetelmäksi GradientBoostingRegressor ja ristiinvalidoinniksi 3-fold. Määritetään menetelmän optimoitavat parametrit ja niille kokeiltavat arvot sekä validoinnissa käytettävä hyvyysfunktio. Minimoitavaksi häviöfunktioksi valitaan virhetermien itseisarvojen mediaani, mutta koska funktio GridSearchCV maksimoi mittariaan (score), pitää mittariksi valita virhetermien itseisarvojen mediaanin vastaluku (neg_median_absolute_error). Optmoitavat parametrit välitetään GridSearchCV-funktiolle sanakirjamuotoisella parametrilla (tuned_parameters). Kun optimointi on tehty, katsotaan, millaisen GradientBoostingRegressor-menetelmän 
# GridSearchCV-funktio löysi. Funktion GridSearchCV suorittama tyhjentävä haku ja ristiinvalidointi kuluttavat erittäin paljon CPU-aika, jos optimoitaville parametreille kokeiltavia kombinaatioita on paljon, ja siksi tässä esimerkissä optimoitaville parametreille annetaan todella vähän kokeiltavia arvoja. Katsotaan lopuksi löydetyn menetelmän virhe ja miltä ennustukset näyttävät suhteessa todellisiin arvoihin myös tällä menetelmällä. Voidaan todeta, että ainakin mediaanilla mitattuna optimoitu GradientBoostingRegressor-menetelmä tuotti huomattavasti edellä kokeiluja menetelmiä paremman tuloksen, vaikka optimointia ei käytännössä tehty. Todennäköisesti menetelmän hyperparametreihin oli osattu antaa hyvät sivistyneet arvaukset.

# In[ ]:


import sklearn
print('The scikit-learn version is {}.'.format(sklearn.__version__))

#sorted(sklearn.metrics.SCORERS.keys())


# In[ ]:


n_est = 500

tuned_parameters = {
    "n_estimators": [ n_est ],
    "max_depth" : [ 4 ],
    "learning_rate": [ 0.01 ],
    "min_samples_split" : [ 2 ],
    "loss" : [ 'ls', 'lad' ]
}

gbr = ensemble.GradientBoostingRegressor()
clf = GridSearchCV(gbr, cv=3, param_grid=tuned_parameters,
        scoring='neg_median_absolute_error')
preds = clf.fit(X_train, y_train)
best_gbr = clf.best_estimator_
best_gbr


# In[ ]:


abs(clf.best_score_)


# In[ ]:


pd.DataFrame({'Price' : y_test, 'Best GBR' : best_gbr.predict(X_test)})


# Tarkastellaan vielä, kuinka jokainen boosting-kierros vaikuttaa menetelmän virheeseen, jotta nähdään, kannattaisiko iteraatioiden määrää kasvattaa GradientBoostingRegressor-menetelmässä. Optimoinnin valitsemassa menetelmässä oli käytössä tappiofunktiona pienin absoluuttinen poikkeama (LAD), joka minimoi virhetermien itseisarvojen summaa ja toimii tässä pienintä nelisummaa paremmin (jos uskotaan optimoinnin olevan oikeassa). Kuvasta näkyy, että poikkeama alkaa tasaantua 300-400 iteraation kohdalla, jonka jälkeen menetelmän sovitusvirhe ja siten myöskään ennustustulos ei enää merkittävästi parane. Tein sovituksen 500 iteraatiolla.

# In[ ]:


# plot error for each round of boosting
test_score = np.zeros(n_est, dtype=np.float64)
train_score = best_gbr.train_score_

for i, y_pred in enumerate(best_gbr.staged_predict(X_test)):
    test_score[i] = best_gbr.loss_(y_test, y_pred)
    
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(np.arange(n_est), train_score, 'darkblue', label='Training Set Error')
plt.plot(np.arange(n_est), test_score, 'red', label='Test Set Error')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Least Absolute Deviation')


# Menetelmää voisi yrittää vielä parantaa määrittelemällä optimoitaville parametreille enemmän tutkittavia arvoja, mutta siihen tarvittaisiin paljon laskentakapasiteettia eli käytännössä laskenta pitäisi hajauttaa johonkin klusteriin. Esimerkissä ohjeistettiin käyttämään pakettia spark-sklearn optimoinnin hajauttamiseksi Spark-klusteriin.
# 
# Tarkastellaan lopuksi vielä eri muuttujien merkitystä löydetyssä mallissa vertailemalla niiden merkityksiä merkitykseltään suurimpaan muuttujaan. Alla olevasta kuvasta nähdään, että merkittävimmät muuttujat ovat 'Private room', 'accommodates', 'availability_30', 'Innere Stadt' ja 'bedrooms', joista merkittävin (Private room) vaikuttaa hintaan negatiivisesti ja muut positiivisesti. Vaikutusten suunta on helppo tarkastaa visualisoinnin yhteydessä lasketuista korrelaatioista, sillä jokaisella näistä muuttujista oli riittävän vahva korrelaatio hinnan kanssa tämän päättelemiseksi. Kuten aiemmin totesin yksityinen huone kuvaa muuttujana kohtuullisen suoraan kokonaisen huoneiston vastakohtaa, joten suurin hintaennuste on kokonaan käytössä olevilla asunnoilla, joissa on suuri majoituskapasiteetti ja monta makuuhuonetta, ja jotka ovat usein saatavilla ja sijaitsevat ydinkeskustassa - ei kovin yllättävä tulos.

# In[ ]:


feature_importance = clf.best_estimator_.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
sorted_idx = sorted_idx[sorted_idx.size-15:sorted_idx.size]
pos = np.arange(sorted_idx.shape[0]) + .5
pvals = feature_importance[sorted_idx]
pcols = X_train.columns[sorted_idx]

plt.figure(figsize=(8,10))
plt.barh(pos, pvals, align='center')
plt.yticks(pos, pcols)
plt.xlabel('Relative Importance')
plt.title('Variable Importance')


# Tein lopuksi vielä menetelmiä LinearRegression ja GradientBoostingRegressor käyttäen uudet koneoppimismallit, joihin otin mukaan vain nämä viisi edellä mainittua muuttujaa. Näiden mallien avulla voi harjoitustyön lopussa ennustaa kohteen hintaa käyttäjän antaman syötteen perusteella. Myös arvioiden määrä ja arviolukema vaikuttaa hintaan jonkun verran, mutta jätin nämä näistä uusista ennustemalleista, sillä kyseisiä tietoja ei ole saatavissa uusista kohteista. Ainakaan mediaanivirheet eivät kasvaneet merkittävästi, vaikka selittäjämuuttujien määrän tiputti viiteen.

# In[ ]:


short_feature_matrix = alldata[['Private room', 'accommodates', 'availability_30', 
                                'Innere Stadt', 'bedrooms']]
model_linear = linear_model.LinearRegression()
F_train, F_test, p_train, p_test = train_test_split(short_feature_matrix, alldata.price,
                                                    test_size=0.2, random_state=20)

model_linear.fit(F_train, p_train)
print("Kertoimet: ", model_linear.coef_)

metrics.median_absolute_error(y_test, e.predict(X_test))


# In[ ]:


preds = clf.fit(F_train, p_train)
model_gbr = clf.best_estimator_
model_gbr


# In[ ]:


abs(clf.best_score_)


# In[ ]:


model_gbr.feature_importances_/model_gbr.feature_importances_.max()


# In[ ]:


pd.DataFrame({'Price' : p_test, 'Linear reg.' : model_linear.predict(F_test),
                                'Gradient boost' : model_gbr.predict(F_test)})


# ### 6. Toimeenpano
# 
# Tein siivotusta datasta Powor BI -ohjelmistolla vuorovaikutteisen [dashboardin](https://app.powerbi.com/groups/me/dashboards/13039dda-a39a-4a53-b01a-eb80b0324df8?ctid=fa6944af-cc7c-4cd8-9154-c01132798910), jonka avulla vuokrauskohteita voi suodataa kaupunginosan, hinnan, majoituskapasiteetin, vuoteiden lukumäärän, makuuhuoneiden lukumäärän ja vuokrauskohteen tyypin perusteella. Kohteiden wep-sivulinkit ovat mukana, joten kohteiden tarkempiin tietoihin pääsee porautumaan suoraan kartasta klikkaamalla. Sivu avautuu uuteen välilehteen selaimessa. Dashboardin avulla matkailija voi hakea sopivaa majoituskohdetta eri kriteerien perusteella. Majoitusbisnestä pyörittävä voi puolestaan, tarkastella, mistä ja millaisen majoituskapasiteetin vuokrauskohteita kannattaa hankkia. Matkustajille oheispalveluita myyvä yrittäjä voi puolestaan tarkastella, missä olisi eniten hänen palveluidensa kohderyhmille sopivia vuokrauskohteita tarjolla. Kiinteistösijoittajan käyttöön aineiston data on mielestäni puutteellista, mutta omaa asuntoa etsivä voi käyttää dashboardia myös välttääkseen Airbnb-keskittymän tulevassa naapurustossaan. Jos Wienissä haluaisi pyörittää Airbnb-bisnestä, niin analyysin perusteella kannattaisi hankkia ydinkeskustasta majoituskapasiteetiltaan hyvä asunto ja vuokarata sitä yhtenä kokonaisuutena. Analyysi ei kyllä pysty mitenkään vertailemaan sellaisia tilanteita, joissa sama huoneisto vuokrattaisiin joko osina tai kokonaisuutena.
# 
# Jukan pitäisi päästä käyttämään dashboardia tuni-tunnuksellaan tuosta toimeenpanokohdan alussa olevasta linkistä. Kartat eivät aina kohdistu heti Wieniin, mutta sivun uudelleen lataamalla niiden pitäisi kohdistua oikein. Pikkukartalla tai pylväsdiagrammeista voi valita tarkasteltavan kaupunginosan, jolloin pääkartta zoomautuu siihen.
# 
# Foliumilla toteuttamiani vuorovaikutteisia karttavisualisointeja voi käyttää samoihin tarkoituksiin, mutta ne eivät ole käytettävyydeltään yhtä helppoja, sillä suodatukset joutuu tekemään aina koodilla dataframeen ja sen jälkeen joutuu generoimaan haluamansa kartan uudestaan. Toki koodatessa suodatuksille on vain mielikuvitus rajana. Myös Foliumilla toteutetussa kohdekartassa on kohteiden linkit mukana, joten siitäkin pääse suoraan tarkastelemaan kohteita. Kohteen sivu avautuu tästäkin kartasta uuteen välilehteen.
# 
# Lopuksi tein vielä pienen interaktiivisen sovelluksen, joka ennustaa viiden muuttujan yksinkertaistetuilla malleilla (model_linear ja model_gbr) Airbnb-kohteen hinnan Wienissä ja tulostaa nämä hinnat. Sovellus kysyy käyttäjältä yksitellen vuokrauskohteen arvot näille viidelle malleissa käytettävälle piirteelle. 

# In[ ]:


def tolist_1_or_0(list, value):
    
    value = value.lower()
    if value in ['y', 'n']:
        list[0] = (value == 'y').real
        return True
    else:
        return False

def tolist_between(list, min, max, value):

    if (value >= min) and (value <= max):
        list[0] = value
        return True
    else:
        return False
    


# In[ ]:


def price_predictor():
    
    features = pd.DataFrame({'Private room' : [0], 'accommodates' : [0],
                             'availability_30' : [0], 'Innere Stadt' : [0], 'bedrooms' :[0]
                            })
    while True:
 
        print("To quit give something else asked!")

        try:
            
            if (tolist_1_or_0(features['Private room'], input('Private room (y/n): ')) and
                tolist_1_or_0(features['Innere Stadt'], input('Innere Stadt (y/n): ')) and
                tolist_between(features['accommodates'], 1, 20, 
                               int(input('Acommodates (1..20): '))) and
                tolist_between(features['bedrooms'], 1, 10,
                               int(input('Bedrooms (1..10): ')))    and
                tolist_between(features['availability_30'], 1, 30, 
                               int(input('Availability in a month (1..30): ')))
               ):
            
                print('\nPredicted price according gradient boosting regressor    :',
                      round(model_gbr.predict(features)[0], 1), '$'
                      '\nPredicted price according least square linear regression :', 
                      round(model_linear.predict(features)[0], 1),'$\n')            
            else:
                break
            
        except Exception:
            break
            
    print('Exit')
        


# In[ ]:


price_predictor()

