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


from wtforms import RadioField, SelectMultipleField, TextField, IntegerField
from flask.ext.wtf import Form, validators
from wtforms.validators import ValidationError, Required, Regexp

#import settings

#class CmipButton(Form):
  #example = RadioField('Label', choices=[('value_one','CMIP 3'),('value_two','CMIP 5')])

#class WacButton(Form):
  #example = RadioField('Label', choices=[('value_one','Warming Attribution'),('value_two','Time Slice')])

#class MyForm(Form):
    #assigned = SelectMultipleField('Assigned', choices=[])
    #available = SelectMultipleField('Available', choices=[('1','1'),('2','2')])


def bounds_check(form, field):
  start,end = [int(t) for t in field.data.split("-")]
  print start,end
  print "sadfasdfasfd"
  if start < 1850 or end > 2014:
    raise ValidationError('Please choose preindustrial period between 1850 and 2014.')

class CmipForm1(Form):
  models = SelectMultipleField(u'Available Models', choices=[],
            validators=[Required("Please select at least one model.")])

class CmipForm2(Form):
  models = SelectMultipleField(u'Selected Models', choices=[],
            validators=[Required("Please select at least one model.")])

class ScenarioForm1(Form):
  scenarios = SelectMultipleField(u'Available Scenarios', choices=[],
                validators=[Required("Please select at least one scenario.")])

class ScenarioForm2(Form):
  scenarios = SelectMultipleField(u'Selected Scenarios', choices=[],
                validators=[Required("Please select at least one scenario.")])

class PeriodField(Form):

  #def period_check(form, field):
    #strper = field.data
    #if len(strper) != 9:
      #raise ValidationError('Please use YYYY-YYYY format for period.')

    #per = strper.split("-")
    #if len(per) != 2:
      #raise ValidationError('Please use "-" as delimiter for period.')

    #try:
      #per = [int(t) for t in per]
    #except ValueError:
      #raise ValidationError('Year numbers are no integers, please use YYYY-YYYY.')

  # regular expression that validates time format like 1940-2000
  regex = "[1-2][0-9]{3}-[1-2][0-9]{3}"

  preindperiod  = TextField(u'Preindustrial Period', validators=[Regexp(regex, message="Please use YYYY-YYYY format."),bounds_check])
  baseperiod    = TextField(u'Projection Base  Period', validators=[Regexp(regex, message="Please use YYYY-YYYY format.")])
  finalperiod   = TextField(u'Projection Final Period', validators=[Regexp(regex, message="Please use YYYY-YYYY format.")])


class WarmingLevelField(Form):

  def timeslice_check(form, field):
    strper = field.data
    try:
      [float(t) for t in field.data.split(",")]
    except Exception, e:
      raise ValidationError('Please use a comma separated list like "1.5,2,2.5" for warming levels')

  def odd_check(form, field):
    print "odd check"
    if field.data % 2 == 0:
      raise ValidationError('Please choose an odd number of years for the averaging period.')

  # regular expression that validates time format like 1940-2000
  regex = "[1-2][0-9]{3}-[1-2][0-9]{3}"

  preindperiod  = TextField(u'Preindustrial Period', validators=[Regexp(regex, message="Please use YYYY-YYYY format."),bounds_check])
  baseperiod = TextField(u'Projection Base  Period', validators=[Regexp(regex, message="Please use YYYY-YYYY format.")])
  wlevels    = TextField(u'Warming Levels', validators=[Required(), timeslice_check])
  av_window  = IntegerField(u'Averaging Window in Years', validators=[Required(), odd_check])



