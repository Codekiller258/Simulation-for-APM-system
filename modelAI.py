from mesa import Model, Agent
from mesa.time import RandomActivation,SimultaneousActivation,BaseScheduler

from mesa.datacollection import DataCollector
import rasterio as rs
import matplotlib.pyplot as plt
import random
import math
import numpy as np
import numpy_financial as nf

# Import the agent class(es) from agents.py
from agentsAI import PhysicalAssetAI, WarehouseAI, MaintenanceAI, UNS, EquipmentAI#, SPO



# Define the OMmodel class
class OMmodelAI(Model):
    """
    The main model running the simulation. I.
    """

    def __init__(self,seed= None,
                 #sorting time(in hours)
                 sorting=3,
                 # failure rate of each component(in hours)
                 f1=20/1000000,f2=30/1000000,f3=40/1000000,f4=50/1000000,f5=60/1000000, fo=100/1000000,
                 #number of spare parts
                 num_spareparts = 10,
                 #number of deliver time from equipment supplier to warehouse (in hours)
                 lead_time = 24,
                 #Maintenance crews's learning time for failure, repair time, planning time, (in hours) and the chance to find failures
                 wisdom_level = 0.5,
                 interest_rate = 0.15,
                 learning_time = 3, repair_time = 3, planning_time=3,
                 profit_per_product = 10,
                 CAPEX_AI = 500000,
                 OPEX_AI = 100000
                 ):
        self.sorting = sorting
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.f5 = f5
        self.fo = fo
        self.num_spareparts = num_spareparts
        self.lead_time = lead_time
        self.learning_time = learning_time
        self.learning_time = learning_time
        self.repair_time = repair_time
        self.planning_time = planning_time
        self.wisdom_level = wisdom_level
        self.interest_rate = interest_rate
        self.profit_per_unit = profit_per_product



        #Some states for KPIs
        self.downtime = 0
        self.WorkingHourInYear = 0
        self.financial_list_year = []
        self.production_per_hour = 500

        self.normal_maintenance_fee = 3000
        self.downtime_inyear = 0
        self.MTTF_list=[]
        self.MTTR_list=[]
        self.MTTF = 0
        self.MTTR = 0
        self.Availability = 0
        self.OEE = 0
        self.NPV = 0
        self.CAPEX_AI = CAPEX_AI
        self.OPEX_AI = OPEX_AI



        super().__init__(seed = seed)
        self.seed = seed
        
        

        physical_asset = PhysicalAssetAI(unique_id=1, model=self, seed=self.seed)
        warehouse=WarehouseAI(unique_id=2, model=self, seed=self.seed)
        maintenance_crew = MaintenanceAI(unique_id=4, model=self, seed=self.seed)
        Uns = UNS(unique_id=5, model=self, seed=self.seed)
        supplier = EquipmentAI(unique_id=6, model=self, seed=self.seed)

        
        self.schedule = SimultaneousActivation(self) 
        self.schedule.add(physical_asset)
        self.schedule.add(warehouse)
        self.schedule.add(Uns)
        #self.schedule.add(operation_crew)
        self.schedule.add(maintenance_crew)

        self.schedule.add(supplier)
        model_metrics = {
                        
                        "Downtime" : 'downtime',
                        "NPV":"NPV",
                        "OEE":"OEE",
                        "MTTF":"MTTF",
                        "MTTR":"MTTR",
                        "Availability":"Availability",



                        
                        }
        self.datacollector = DataCollector( model_reporters=model_metrics)


        
    def down_time (self): 
            for agent in self.schedule.agents:
                if isinstance(agent,PhysicalAssetAI) and agent.is_working == False:
                    self.downtime +=1
                    return self.downtime
    
    def financial(self):
        for agent in self.schedule.agents:
                if isinstance(agent,PhysicalAssetAI) and agent.is_working == True:
                    self.WorkingHourInYear += 1
        if self.schedule.steps == 0:
                    earning_in_year = -self.CAPEX_AI
                    self.financial_list_year.append(earning_in_year)
        if (self.schedule.steps + 1) % (365*8) == 0:
                for agent in self.schedule.agents:
                     if isinstance(agent, PhysicalAssetAI):
                          spare_cost = agent.spareparts_use_counting * 2000
                          # The AI based models have the cost for Captital investment for AI 
                          # and yearly service fee
                          before_tax_earning_in_year = self.WorkingHourInYear*self.production_per_hour\
                            *self.profit_per_unit*0.97*0.9-self.OPEX_AI-spare_cost
                          tax= 0.25 * before_tax_earning_in_year
                          earning_in_year = before_tax_earning_in_year - tax
                          self.financial_list_year.append(earning_in_year)
                          self.WorkingHourInYear = 0
                          agent.spareparts_use_counting = 0
    
    def system_KPIs(self):
         if self.schedule.steps == 10*365*8-1:
            if len(self.MTTF_list) ==0:
                 self.MTTF_list = [10*365*8]
            if len(self.MTTR_list) ==0:
                 self.MTTR_list = [self.learning_time+self.planning_time+self.repair_time]
            self.MTTF=sum(self.MTTF_list)/len(self.MTTF_list)
            self.MTTR= sum(self.MTTR_list)/len(self.MTTR_list)
            self.NPV=nf.npv(self.interest_rate,self.financial_list_year)
            self.Availability=(self.schedule.steps-self.downtime)/self.schedule.steps
            self.OEE = self.Availability * 0.9 * 0.97

    
    def step(self):
        self.down_time()
        self.financial()
        self.system_KPIs()
        self.datacollector.collect(self)
        self.schedule.step()   

        