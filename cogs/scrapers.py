import datetime
import discord
import requests
from bs4 import BeautifulSoup
from time import perf_counter
from logger import my_logger
from discord.ext import commands

log = my_logger()
    
class Scrapers(commands.Cog):
    """İnternetten çektiği verileri gösteren komutlar"""
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def namazgonder(self):
        timer_start = perf_counter()
        r = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/9609/kastamonu-icin-namaz-vakti",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
        log.INFO(f"Got 1 page in {perf_counter() - timer_start} seconds.")
        source = BeautifulSoup(r.content,"html.parser")
        tarih = source.find("div",attrs={"class":"ti-hicri"})
        tarih = tarih.text
        tarih = tarih.replace("\n","")
        imsak = source.find("div",attrs={"data-vakit-name":"imsak"}).find("div",attrs={"class":"tpt-time"}).text
        imsak = "İmsak Vakti : "+imsak+"\n"
        gunes = source.find("div",attrs={"data-vakit-name":"gunes"}).find("div",attrs={"class":"tpt-time"}).text
        gunes = "Güneş Vakti : "+gunes+"\n"
        oglen = source.find("div",attrs={"data-vakit-name":"ogle"}).find("div",attrs={"class":"tpt-time"}).text
        oglen = "Öğlen Vakti : "+oglen+"\n"
        ikindi = source.find("div",attrs={"data-vakit-name":"ikindi"}).find("div",attrs={"class":"tpt-time"}).text
        ikindi = "İkindi Vakti : "+ikindi+"\n"
        aksam = source.find("div",attrs={"data-vakit-name":"aksam"}).find("div",attrs={"class":"tpt-time"}).text
        aksam = "Akşam Vakti : "+aksam+"\n"
        yatsi = source.find("div",attrs={"data-vakit-name":"yatsi"}).find("div",attrs={"class":"tpt-time"}).text
        yatsi = "Yatsı Vakti : "+yatsi+"\n"
        vakit = imsak+gunes+oglen+ikindi+aksam+yatsi
        return vakit

    def fiyatlar(self):
        t1_start = perf_counter()

        main_page = BeautifulSoup(requests.get("https://www.bloomberght.com/").content,"html.parser")

        usd     = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'USDTRY Curncy'}).get_text()
        eur     = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'EURTRY Curncy'}).get_text()
        gbp     = main_page.find('tr', class_='tab-content-bottom-list live-ingiliz-sterlini').find_next('td', class_='LastPrice').text
        ceyrek  = main_page.find('tr', class_='tab-content-bottom-list live-gram-altin').find_next('td', class_='LastPrice').text
        bist    = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'XU100 Index'}).get_text()
        faiz    = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'TAHVIL2Y'}).get_text()

        log.INFO(f"Got 1 page in {perf_counter() - t1_start} seconds.")

        #final= "USD/TRY: {0}\nEUR/TRY: {1}\nGBP/TRY: {2}\nÇeyrek Satış: {3}\nBIST 100: {4}\nFaiz: {5}".format(usd,eur,gbp,ceyrek,bist,faiz)
        embed = discord.Embed(title="Döviz Kurları", color=0xff0000, description="Son Güncelleme: <t:{0}:t>".format(int(datetime.datetime.now().timestamp())))
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/d/d7/Philippine-stock-market-board.jpg")
        embed.add_field(name="Dolar/TL:", value = usd, inline=True)
        embed.add_field(name="Euro/TL:", value = eur, inline=True)
        embed.add_field(name="Sterlin/TL:", value = gbp, inline=True)
        embed.add_field(name="Çeyrek Alış:", value = ceyrek, inline=True)
        embed.add_field(name="BIST 100:", value = bist, inline=True)
        embed.add_field(name="Faiz:", value = faiz, inline=True)
        return embed

    def benzin_fiyat(self):
        t1_start = perf_counter()
        r = requests.get("https://www.petrolofisi.com.tr/akaryakit-fiyatlari",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
        log.INFO(f"Got 1 page in {perf_counter() - t1_start} seconds.")

        sec = BeautifulSoup(r.content,"html.parser").findAll('li')

        for item in sec:
            if "KASTAMONU" in item.text:
                result = item
                break
            else: 
                pass

        new_soup = BeautifulSoup(result.prettify(),"html.parser")
        for i in new_soup.findAll('div', class_='mt-2'): #Remove child element of <div>'s
            i.find_next().decompose()

        out = new_soup.findAll('div', class_='mt-2')

        list = []
        for tip in out:
            list.append(tip.get_text().strip())
        embed=discord.Embed(title="Akaryakıt Fiyatları", 
        url="https://www.petrolofisi.com.tr/akaryakit-fiyatlari", 
        description="Son Güncelleme: <t:{0}:t>".format(int(datetime.datetime.now().timestamp())), color=0xff0000)
        
        embed.add_field(name="Benzin", value=list[0], inline=True)
        embed.add_field(name="Mazot", value=list[1], inline=True)
        embed.add_field(name="Otogaz", value=list[3], inline=True)
        return embed
    
    @commands.hybrid_command(pass_context=True)
    async def namaz(self, ctx):
        """Namaz vakitlerini gösterir."""
        await ctx.send(self.namazgonder())

    @commands.hybrid_command(pass_context=True)
    async def borsa(self, ctx):
        """Borsa durumunu gönderir."""
        await ctx.send(embed=self.fiyatlar())

    @commands.hybrid_command(pass_context=True)
    async def akaryakıt(self, ctx):
        """Akaryakıt fiyatlarını gönderir."""
        await ctx.send(embed=self.benzin_fiyat())