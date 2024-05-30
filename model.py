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
from agents import PhysicalAsset, Warehouse, Operation_crew, Maintenance_crew, Control_room, SAP,equipment_supplier#, SPO



# Define the OMmodel class
class OMmodel(Model):
    """
    The main model running the simulation. I.
    """

    def __init__(self,seed= None,
                 #sorting time(in hours)
                 sorting=3,
                 # failure rate of each component(in hours)
                 f1=20/1000000,f2=30/1000000,f3=40/1000000,f4=50/1000000,f5=60/1000000, fo = 100/1000000,
                 #number of spare parts
                 num_spareparts = 10,
                 #number lead time
                 lead_time = 24,
                 #Maintenance crews's learning time for failure, repair time, planning time, (in hours) and the chance to find failures
                 learning_time = 5, repair_time = 10, planning_time = 3, chance_to_find_failure_in_schedule = 0.8,
                 #sceduled maintenance interval and shceduled maintenance time (in hours)
                 maintenance_interval = 3*30*8, repairtime_scheduledmaintenance = 8,
                 interest_rate = 0.15,
                 profit_per_product = 10
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
        self.repair_time = repair_time
        self.planning_time = planning_time
        self.chance_to_find_failure_in_schedule = chance_to_find_failure_in_schedule
        self.maintenance_interval = maintenance_interval
        self.repairtime_scheduledmaintenance = repairtime_scheduledmaintenance
        self.interest_rate = interest_rate
        

        #Some states for KPIs
        self.downtime = 0
        self.WorkingHourInYear = 0
        self.financial_list_year = []
        self.production_per_hour = 500
        self.profit_per_unit = profit_per_product
        self.schedule_maintenance_fee = 2000
        self.normal_maintenance_fee = 3000
        self.downtime_inyear = 0
        self.MTTF_list=[]
        self.MTTR_list=[]
        self.MTTF = 0
        self.MTTR = 0
        self.Availability = 0
        self.OEE = 0
        self.NPV = 0

        super().__init__(seed = seed)
        self.seed = seed
        
        
        physical_asset = PhysicalAsset(unique_id=1, model=self, seed=self.seed)
        warehouse=Warehouse(unique_id=2, model=self, seed=self.seed)
        operation_crew = Operation_crew(unique_id=3, model=self, seed=self.seed)
        maintenance_crew = Maintenance_crew(unique_id=4, model=self, seed=self.seed)
        control_room = Control_room(unique_id=5, model=self, seed=self.seed)
        sap = SAP(unique_id=6, model=self, seed=self.seed)
        supplier = equipment_supplier(unique_id=7, model=self, seed=self.seed)

        
        # Add different agent into the scheduler
        self.schedule = SimultaneousActivation(self) 
        self.schedule.add(physical_asset)
        self.schedule.add(warehouse)
        self.schedule.add(sap)
        self.schedule.add(operation_crew)
        self.schedule.add(maintenance_crew)
        self.schedule.add(control_room)
        self.schedule.add(supplier)

        
        #Define KPIs to be outputted
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
                if isinstance(agent,PhysicalAsset) and agent.is_working == False:
                    self.downtime +=1
    
    def financial(self):
        for agent in self.schedule.agents:
                if isinstance(agent,PhysicalAsset) and agent.is_working == True:
                    # Get yearly working hours.
                    self.WorkingHourInYear += 1
        if self.schedule.steps == 0:
             earning_in_year = 0
             self.financial_list_year.append(earning_in_year)
        # Assume everyday work 8 hours, at each end of the year the financial will be calculated
        if (self.schedule.steps + 1) % (365*8) == 0:
                schedule_cost_year = self.schedule_maintenance_fee * (365*8)/self.maintenance_interval
                for agent in self.schedule.agents:
                     if isinstance(agent, PhysicalAsset):
                          # The yearly spare parts use is calculated in PhysicalAsset class
                          spare_cost = agent.spareparts_usenumber_count * 2000
                # Cash flow each year = working hours * production per hour * performance * quality
                #* profit per product - scheduled maintenance fee - spare part costs
                before_tax_earning_in_year = self.WorkingHourInYear*(self.production_per_hour*0.95*0.8)\
                    *self.profit_per_unit-schedule_cost_year - spare_cost
                # Tax will also be considered
                tax = 0.25 * before_tax_earning_in_year
                earning_in_year = before_tax_earning_in_year - tax
                self.financial_list_year.append(earning_in_year)
                # Working hour reset at the end of each year
                self.WorkingHourInYear = 0
    
    def system_KPIs(self):
         # KPIs will be calculated at the end of the 10-year study period
         if self.schedule.steps == 10*365*8-1:
            # MTTF = total failure time (hours) / the number of failure
            self.MTTF=sum(self.MTTF_list)/len(self.MTTF_list)
            # MTTR = total repair time (hours) / the number of failure
            self.MTTR= sum(self.MTTR_list)/len(self.MTTR_list)
            self.NPV=nf.npv(self.interest_rate,self.financial_list_year)
            # Availability = (total time - downtime) / total time
            self.Availability=(self.schedule.steps-self.downtime)/self.schedule.steps
            # OEE = availability * performance * quality rate
            self.OEE = self.Availability * 0.8 * 0.95




    def step(self):

        self.down_time()
        self.financial()
        self.system_KPIs()
        self.datacollector.collect(self)
        self.schedule.step()

        