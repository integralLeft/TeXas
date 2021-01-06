import discord
import subprocess
import asyncio
import logging
from discord.ext import commands
from discord.ext.commands import Bot
import traceback
import sys

from sympy import *
x, y, z, t, a, b, c = symbols('x y z t a b c')

import os
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

import csv

description = """TeXas"""

help_message = '```TeXas help \n----------------------\n latex: render LaTeX \n solve: solve expressions with SymPy\n\nExamples:\n----------------------\n latex \int_{-\infty}^\infty \\frac{1}{\sqrt{2\pi}} e^{-\\frac{x^2}{2}}\; \\text{d}x\n solve integrate((E**(-x**2/2))/sqrt(2*pi),(x,-oo,oo))```'

inline_bot = discord.Client()

@inline_bot.event
async def on_ready():
    print('logged in as: ')
    print(inline_bot.user.name)
    print(inline_bot.user.id)
    print('-----')
    activity = discord.Activity(name='for "TeXas help"', type=discord.ActivityType.watching)
    await inline_bot.change_presence(activity=activity)

def PNGify(latex):
    ## read user input (argument) as a latex equation
    le = "$$" + latex + "$$"
    ## skeleton for latex .tex file
    before_eq_string = r"\documentclass{article} \usepackage{amsmath} \usepackage{amssymb} \begin{document} \thispagestyle{empty} \setlength{\parindent}{0pt}"
    after_eq_string = r"\end{document}"
    ## set latex_filename parameter
    lf = "tempfile"
    ## create the .tex file from the skeleton
    tex_file_contents = before_eq_string + le + after_eq_string
    tex_file = open(lf + ".tex", "w")
    tex_file.write(tex_file_contents)
    tex_file.close()
    ## create the pdf (`pdflatex -jobname='filename to write' file.tex`)
    # to specify output name: -jobname=STRING flag before the FILE flag at the end
    os.system('pdflatex ' + lf + '.tex > /dev/null 2>&1')
    ## crop the pdf to remove excess whitespace
    os.system('pdfcrop -margin 3 ' + lf + '.pdf ' + lf + '.pdf > /dev/null 2>&1')
    ## create the png from the pdf (`convert -density 3000 file.pdf -quality 90 file.png`)
    os.system('convert -quiet -density 3000 -background white -alpha remove -alpha off ' + lf + '.pdf -quality 90 ' + lf + '.png')
    ## remove all the useless (.aux, .log, .pdf, .tex) latex files
    os.system('rm ' + lf + '.log ' + lf + '.aux ' + lf + '.pdf ' + lf + '.tex')
    return lf + '.png'

def SOLVE(math_string):
    return latex(eval(math_string))

@inline_bot.event
async def on_message(message):
    if message.author.bot:
        return
    content = message.content
    reply = ''
    if content[:6] == 'latex ':
        # turn latex code into a PNG
        reply += PNGify(content[6:])
    elif content[:6] == 'solve ':
        # turn math into PNG result
        reply += PNGify(SOLVE(content[6:]))
    elif content == 'TeXas help':
        await message.channel.send(help_message)
        return
    if reply != '':
        await message.channel.send(file=discord.File(reply))
        os.system('rm ' + reply)

inline_bot.run(TOKEN)

