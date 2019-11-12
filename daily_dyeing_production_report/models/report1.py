# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from odoo import api, fields, models

class dailydyeingReport(models.TransientModel):

    
    _name = 'daily.dyeing.report'
    _description = 'Daily Dyeing Report'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    
    pan= fields.Many2one('dyingprocess.form', string='Pan')
    
    

    @api.multi
    def print_report_dailydyeing_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
             'model': 'report.model',
             'form': self.read()[0]
        }
        return self.env['report'].get_action(self, 'daily_dyeing_production_report.dailydyeing_report',data=datas)


class Reportdailydyeing(models.AbstractModel):
    _name = 'report.daily_dyeing_production_report.dailydyeing_report' #report.modulename.your_modelname of report
    
    main_list=[]

    
    def OurFunc(self,name):
        if len(self.main_list) == 0:
            return -1
        index = 0
        for items in self.main_list:
            if items[0] == name:
                return index
            index+=1

        return -1
    
    @api.multi
    def render_html(self, docids, data=None):

        daily = self.env["mrp.production"].search([('date_planned_start','<=',data['form']['date_to']),('date_planned_start','>=',data['form']['date_from']),('state','=','done')])
        daily1 = self.env["dyingtype.form"].search([])

        my_list=[0,0,0]
        del self.main_list[:]
        for e in daily:
            index = self.OurFunc(e.dying_type.name)
            if index == -1:
                my_list[0] = e.dying_type.name
                my_list[1] = float(e.bundle)
                my_list[2] = float(e.weight1)
                self.main_list.append(my_list[:])
            else:
                self.main_list[index][1] += float(e.bundle)
                self.main_list[index][2] += float(e.weight1)
            
        docargs = {
            'datav':daily,
            'datab':daily1,
            'date_planned_start':data['form']['date_to'],
            'date_planned_start2':data['form']['date_from'],
            'list1':self.main_list
            
        }
        return self.env['report'].render('daily_dyeing_production_report.dailydyeing_report',docargs)

          

