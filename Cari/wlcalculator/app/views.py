# Copyright (C) 2014 Matthias Mengel and Carl-Friedrich Schleussner
#
# This file is part of wacalc.
#
# wacalc is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# wacalc is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with wacalc; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from app import app
from flask import redirect, render_template, url_for, request, flash, get_flashed_messages, g, session
from collections import OrderedDict
from werkzeug.routing import BuildError
import settings
import forms
import numpy as np
import wacalc.CmipData as CmipData; reload(CmipData)
import wacalc.hadcrut_warming as hadcrut_warming; reload(hadcrut_warming)
#import wacalc.warming_level as wl; reload(wl)
#import wacalc.data2 as data2; reload(data2)

attrchoice = ['Warming attribution','Exceedance time for warming levels']
cmipchoice = ['CMIP3', 'CMIP5']
cmip3models = sorted([x.lower() for x in settings.cmip3_models])
cmip5models = sorted([x.lower() for x in settings.cmip5_models])
cmip3scens  = sorted([x.lower() for x in settings.cmip3_scenarios])
cmip5scens  = sorted([x.lower() for x in settings.cmip5_scenarios])
cmipmodels = {"CMIP3":cmip3models, "CMIP5":cmip5models}
scenarios  = {"CMIP3":cmip3scens, "CMIP5":cmip5scens}
wperiod_average_window = 31
#hadcrut_path  = "../../data/hadcrut_v001/"

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field: %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/')
def index():
  session["attr_chosen"]   = attrchoice[0]
  session["cmip_chosen"]   = cmipchoice[1]
  session["models_chosen"]  = []
  session["scens_chosen"]   = []
  session["preindperiod"]  = settings.preindperiod
  session["baseperiod"]    = settings.baseperiod
  session["finalperiod"]   = settings.finalperiod
  session["warminglevels"] = settings.warminglevels
  session["av_window"]     = wperiod_average_window
  print session["warminglevels"]

  return redirect(url_for("choices"))

@app.route('/choices')
def choices():
  form_a = forms.CmipForm1(request.form)#forms.MyForm(request.form)
  form_s = forms.CmipForm2(request.form)#forms.MyForm(request.form)

  try:
    form_a.models.choices = zip(cmipmodels[session["cmip_chosen"]],cmipmodels[session["cmip_chosen"]])
  except KeyError:
    # if people access /choices directly
    return redirect(url_for("index"))

  form_s.models.choices = zip(session["models_chosen"],session["models_chosen"])
  ## for preselection, do
  #form_a = forms.CmipForm1(request.form, models = settings.cmip5models[0:4])
  form_sca = forms.ScenarioForm1(request.form)
  form_scs = forms.ScenarioForm2(request.form)
  form_sca.scenarios.choices = zip(scenarios[session["cmip_chosen"]],scenarios[session["cmip_chosen"]])
  form_scs.scenarios.choices = zip(session["scens_chosen"],session["scens_chosen"])
  pp = "-".join(str(t) for t in session["preindperiod"])
  bp = "-".join(str(t) for t in session["baseperiod"])
  fp = "-".join(str(t) for t in session["finalperiod"])
  wl = ", ".join(str(w) for w in session["warminglevels"])
  print wl
  form_period = forms.PeriodField(request.form, baseperiod=bp, finalperiod=fp, preindperiod=pp)
  form_wlevel = forms.WarmingLevelField(request.form, baseperiod=bp, preindperiod=pp, wlevels=wl, av_window=session["av_window"])
  print form_wlevel.data

  return render_template('choices.html', attrchoice=attrchoice, cmipchoice=cmipchoice,
                          attr_chosen=session["attr_chosen"], cmip_chosen=session["cmip_chosen"], form_period=form_period,
                          form_a=form_a, form_s=form_s, form_sca=form_sca, form_scs=form_scs, form_wlevel=form_wlevel)


@app.route("/attrchoice", methods=("POST", ))
def add_attrchoice():
  print request.form['attrchoice']
  session["attr_chosen"] = request.form['attrchoice']
  return redirect(url_for("choices"))


@app.route("/cmipchoice", methods=("POST", ))
def add_cmipchoice():
  print request.form['cmipchoice']
  session["cmip_chosen"] = request.form['cmipchoice']
  return redirect(url_for("choices"))


@app.route('/modelchoice',  methods=("POST", ))
def add_modelchoice():

  form_a = forms.CmipForm1(request.form)
  form_a.models.choices = zip(cmipmodels[session["cmip_chosen"]],cmipmodels[session["cmip_chosen"]])
  form_s = forms.CmipForm2(request.form)
  if form_a.validate_on_submit():
    session["models_chosen"] = form_a.models.data
    form_s.models.choices = zip(session["models_chosen"],session["models_chosen"])
  else:
    flash_errors(form_a)

  return redirect(url_for("choices"))


@app.route('/scenariochoice',  methods=("POST", ))
def add_scenariochoice():

  form_sca = forms.ScenarioForm1(request.form)
  form_sca.scenarios.choices = zip(scenarios[session["cmip_chosen"]],scenarios[session["cmip_chosen"]])
  form_scs = forms.ScenarioForm2(request.form)

  if form_sca.validate_on_submit():
    session["scens_chosen"] = form_sca.scenarios.data
    form_scs.scenarios.choices = zip(session["scens_chosen"],session["scens_chosen"])
  else:
    flash_errors(form_sca)
    print form_sca.errors
    print form_sca.scenarios.choices

  return redirect(url_for("choices"))


@app.route('/periodchoice',  methods=("POST", ))
def add_periodchoice():

  form_period = forms.PeriodField(request.form)

  if form_period.validate_on_submit():
    session["preindperiod"] = [int(t) for t in form_period.preindperiod.data.split("-")]
    session["baseperiod"]   = [int(t) for t in form_period.baseperiod.data.split("-")]
    session["finalperiod"]  = [int(t) for t in form_period.finalperiod.data.split("-")]

  else:
    flash_errors(form_period)

  return redirect(url_for("choices"))


@app.route('/warminglevelchoice',  methods=("POST", ))
def add_warmingchoice():

  form_wlevel = forms.WarmingLevelField(request.form)

  if form_wlevel.validate_on_submit():
    session["preindperiod"]  = [int(t) for t in form_wlevel.preindperiod.data.split("-")]
    session["baseperiod"]    = [int(t)   for t in form_wlevel.baseperiod.data.split("-")]
    session["warminglevels"] = [float(t) for t in form_wlevel.wlevels.data.split(",")]
    session["av_window"]     = form_wlevel.av_window.data
    print session["av_window"]
  else:
    flash_errors(form_wlevel)

  return redirect(url_for("choices"))


@app.route('/attribution_results',  methods=("GET", "POST", ))
def calc_attribution():

  if request.method == 'GET' and app.debug:
    redirect(url_for("attribution_results"))

  if request.method == 'GET':
    try:
      redirect(url_for("attribution_results"))
    except BuildError:
      redirect(url_for("index"))

  s = session

  if s["models_chosen"] == []:
    flash("Please select a model or a set of models.")

  if s["scens_chosen"] == []:
    flash("Please select a scenario or a set of scenarios.")

  if s["models_chosen"] == [] or s["scens_chosen"] == []:
    return redirect(url_for("choices"))

  cmipdata = CmipData.CmipData(s["cmip_chosen"],s["models_chosen"],s["scens_chosen"])

  try:
    cmipdata.get_cmip()
    cmipdata.compute_warming(s["preindperiod"],s["baseperiod"],s["finalperiod"])
    cmipdata.create_wb3_wlevel_forhtml(settings.warming_levels_wb3, settings.warming_level_names)
  except CmipData.CmipDataException, e:
    flash(str(e))
    return redirect(url_for("choices"))

  bp = "-".join(str(t) for t in s["baseperiod"])
  fp = "-".join(str(t) for t in s["finalperiod"])
  pp = "-".join(str(t) for t in s["preindperiod"])

  mstr = ", ".join(cmipdata.modelavail)

  return render_template('attribution_results.html', bp=bp, fp=fp, pp=pp,
                          cmipdata=cmipdata, mstr=mstr, cmip=s["cmip_chosen"])


@app.route('/timeperiod_results',  methods=("GET", "POST", ))
def calc_timeperiods():

  if request.method == 'GET' and app.debug:
    redirect(url_for("timeperiod_results"))

  if request.method == 'GET':
    try:
      redirect(url_for("timeperiod_results"))
    except BuildError:
      redirect(url_for("index"))

  s = session
  #mc = session["models_chosen"]
  #sc = session["scens_chosen"]
  #bs = session["baseperiod"]
  #ws = session["warminglevels"]
  #av = session["av_window"]
  #cm = session["cmip_chosen"]

  if s["models_chosen"] == []:
    flash("Please select a model or a set of models.")

  if s["scens_chosen"] == []:
    flash("Please select a scenario or a set of scenarios.")

  if s["models_chosen"] == [] or s["scens_chosen"] == []:
    return redirect(url_for("choices"))

  cmipdata = CmipData.CmipData(s["cmip_chosen"],s["models_chosen"],s["scens_chosen"])

  try:
    cmipdata.get_cmip()
    cmipdata.compute_period(s["baseperiod"],s["preindperiod"],
                            s["warminglevels"],window=s["av_window"])
  except CmipData.CmipDataException, e:
    flash(str(e))
    return redirect(url_for("choices"))

  bp = "-".join(str(t) for t in s["baseperiod"])
  pp = "-".join(str(t) for t in s["preindperiod"])

  mstr = ", ".join(cmipdata.modelavail)

  return render_template('timeperiod_results.html', cmipdata=cmipdata, mstr=mstr,
                          np=np, ww=s["av_window"], bp=bp, pp=pp, cmip=s["cmip_chosen"])

@app.route('/home',  methods=("GET", ))
def render_home():
  return redirect(url_for("index"))

@app.route('/about',  methods=("GET", ))
def render_about():
  return render_template('about.html')

@app.route('/contact',  methods=("GET", ))
def render_contact():
  return render_template('contact.html')

@app.route('/documentation',  methods=("GET", ))
def render_docu():
  return render_template('documentation.html')

