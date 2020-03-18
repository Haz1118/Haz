import discord
import asyncio
import openpyxl
import random
import urllib
import requests
import bs4
import os
import sys
import json
import time
import datetime
from selenium import webdriver
from discord import opus
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import bot
from urllib.request import urlopen, Request


bot = commands.Bot(command_prefix='!')
token = 'Njg4MDA3MDU2MzkyOTc4NDQz.XmzUTg.zoz-oNIJfx81PqoM6HBPiA0NcsE'

bot.remove_command('help')

@bot.event
async def on_ready():
    option = configparser.ConfigParser()
    option.read('설정.ini')
    status = option['설정']['상태']
    print("디스코드 봇 실행완료")
    print(bot.user.name)
    print(bot.user.id)
    print('---------')
    game = discord.Game(status)
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await member.send(server, fmt.format(member, server))
async def on_member_remove(member): 
    print('A member has left.')

@bot.command()
async def 도움말(ctx):
    helpbed = discord.Embed(title='도움말',description='롤 정보입니다.',colour=discord.Colour.green())
    helpbed.add_field(name = "!안녕",value = "인사를 해줍니다.",inline=False)
    helpbed.add_field(name = "!초대",value = "초대링크를 알려드려요!.",inline=False)
    helpbed.add_field(name = "!청소",value = "(!청소 숫자) 를 이용해 채팅을 지우세요!",inline=False)
    helpbed.add_field(name = "!핑",value = "핑을 체크 합니다.",inline=False)
    helpbed.add_field(name = "!날씨 ",value = "(!날씨 지역)을 사용하시면 날씨를 알 수 있습니다.",inline=False)
    helpbed.add_field(name = "!롤",value = "(!롤 닉네임)을 사용하여 당신의 전적을 확인하세요!",inline=False) 
    helpbed.add_field(name = "!코로나현황",value = "현재 코로나 현황을 확인합니다.",inline=False)   
    await ctx.send(embed = helpbed)

@bot.command()
async def 안녕(ctx):
    rand = random.randrange(1,4)
    if rand == 1:
        await ctx.send('안녕!, 세상')
    elif rand == 2:
        await ctx.send('뭐')
    elif rand == 3:
        await ctx.send('당근당근')

@bot.command()
async def 초대(ctx):
    await ctx.send('https://discord.gg/8eRT2FZ')

@bot.command()
async def 청소(ctx, num: int =1):
    await ctx.channel.purge(limit=num + 1)
    await ctx.send("청소완료!")
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=1)  

@bot.command()
async def 핑(ctx):
    latancy = bot.latency
    await ctx.send(f'퐁! {round(latancy * 1000)}ms')

@bot.command()
async def 코로나현황(ctx):
    response = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=코로나')
    readerhtml = response.text
    soup = BeautifulSoup(readerhtml, 'lxml')
    data1 = soup.find('div', class_='graph_view')
    data2 = data1.findAll('div', class_='box')
    data3 = data1.findAll('div', class_='box bottom')
    checked = data2[0].find('p', class_='txt').find('strong', class_='num').text
    checking = data2[2].find('p', class_='txt').find('strong', class_='num').text
    free = data3[0].find('p', class_='txt').find('strong', class_='num').text        
    die = data3[1].find('p', class_='txt').find('strong', class_='num').text
    wasup = soup.find('div', class_='csp_notice_info').find('p').find_all(text=True, recursive=True)
    coembed = discord.Embed(color=0x192131, title='코로나현황', description =f'{wasup[1]}' )
    coembed.add_field(name="확진자", value=f'{checked}명', inline=True)
    coembed.add_field(name="격리해제", value=f'{free}명', inline=True)
    coembed.add_field(name="검사중", value=f'{checking}명', inline=True)
    coembed.add_field(name="사망자", value=f'{die}명', inline=True)
    coembed.set_footer(text="https://gist.github.com/SaidBySolo")
    await ctx.send(embed = coembed)

@bot.command()
async def 날씨(ctx, learn):
    location = learn
    enc_location = urllib.parse.quote(location + '날씨')
    
    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%85%BC%EC%82%B0%EB%82%A0%EC%94%A8&oquery='+ enc_location
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    weat = bs4.BeautifulSoup(html, 'html5lib')
    todayBase = weat.find('div', {'class': 'main_info'})

    todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
    todayTemp = todayTemp1.text.strip()  # 온도
    print(todayTemp)

    todayValueBase = todayBase.find('ul', {'class': 'info_list'})
    todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
    todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
    print(todayValue)

    todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
    todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
    print(todayFeelingTemp)

    todayMiseaMongi1 = weat.find('div', {'class': 'sub_info'})
    todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
    todayMiseaMongi3 = todayMiseaMongi2.find('dd')
    todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
    print(todayMiseaMongi)

    tomorrowBase = weat.find('div', {'class': 'table_info weekly _weeklyWeather'})
    tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
    tomorrowTemp2 = tomorrowTemp1.find('dl')
    tomorrowTemp3 = tomorrowTemp2.find('dd')
    tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
    print(tomorrowTemp)

    tomorrowAreaBase = weat.find('div', {'class': 'tomorrow_area'})
    tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
    tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
    tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
    print(tomorrowMoring)

    tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
    tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
    print(tomorrowValue)

    tomorrowAreaBase = weat.find('div', {'class': 'tomorrow_area'})
    tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
    tomorrowAfter1 = tomorrowAllFind[1]
    tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
    tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
    tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
    print(tomorrowAfterTemp)

    tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
    tomorrowAfterValue = tomorrowAfterValue1.text.strip()

    print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

    wbed = discord.Embed(color=0xfaf6f6, title='날씨입니다.')
    wbed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
    wbed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
    wbed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
    wbed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
    wbed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
    wbed.add_field(name='**----------------------------------**',value='**----------------------------------**', inline=False)  # 구분선
    wbed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
    wbed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
    wbed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
    wbed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태
    
    await ctx.send(embed = wbed)

@bot.command()
async def 롤(ctx, nickname):
    location = nickname
    enc_location = urllib.parse.quote(location)

    url = "http://www.op.gg/summoner/userName=" + enc_location
    html = urllib.request.urlopen(url)   

    bsObj = bs4.BeautifulSoup(html, "html.parser") 
    rank1 = bsObj.find("div", {"class": "TierRankInfo"})
    rank2 = rank1.find("div", {"class": "TierRank"})
    rank3 = rank2.text
    print(rank3)

    if rank3 != 'Unranked':
        lolbed1 = discord.Embed(title='롤 정보',description='롤 정보입니다.',colour=discord.Colour.green())      
        lolbed1.add_field(name='당신의 티어', value=rank3, inline=False)
        lolbed1.add_field(name='-당신은 언랭-', value="표시할 전적이 없습니다.", inline=False)
        await ctx.send(embed=lolbed1)
        
    else:
        jumsu1 = rank1.find("div", {"class": "TierInfo"})
        jumsu2 = jumsu1.find("span", {"class": "LeaguePoints"})
        jumsu3 = jumsu2.text
        jumsu4 = jumsu3.strip()#점수표시 (11LP등등)
        print(jumsu4)
 
        winlose1 = jumsu1.find("span", {"class": "WinLose"})
        winlose2 = winlose1.find("span", {"class": "wins"})
        winlose2_1 = winlose1.find("span", {"class": "losses"})
        winlose2_2 = winlose1.find("span", {"class": "winratio"})

        winlose2txt = winlose2.text
        winlose2_1txt = winlose2_1.text
        winlose2_2txt = winlose2_2.text #승,패,승률 나타냄  200W 150L Win Ratio 55% 등등
        print(winlose2txt + " " + winlose2_1txt + " " + winlose2_2txt)

        lolbed2 = discord.Embed(title='롤 정보',description='롤 정보입니다.',colour=discord.Colour.green())
        lolbed2.add_field(name='당신의 티어', value=rank3, inline=False)
        lolbed2.add_field(name='당신의 LP(점수)', value=jumsu3, inline=False)
        lolbed2.add_field(name='당신의 승,패 정보', value=winlose2txt+" "+winlose2_1txt, inline=False)
        lolbed2.add_field(name='당신의 승률', value=winlose2_2txt, inline=False)
        await ctx.send(embed=lolbed2)

bot.run(token)
