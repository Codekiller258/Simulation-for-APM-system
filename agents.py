# import necessary libraries
import math
import random
from mesa import Agent
import numpy as np

# define PhysicalAsset agent
class PhysicalAsset(Agent):
    """
    An agent representing physical asset in the whole APM process.
    """
    def __init__(self, unique_id, model, seed):
        super().__init__(unique_id, model)
        
        # assign basic attributes
        self.is_working = True
        self.working_hours = 0
        self.total_working_time = 0
        self.no_fail = 0
        self.TTR = 0
        
        # define the state of critical component
        self.component1_fail = False
        self.component2_fail = False
        self.component3_fail = False
        self.component4_fail = False
        self.component5_fail = False
        self.componentother_fail = False

        # assign failure rates of components, in hours
        self.failure_rate1 = self.model.f1
        self.failure_rate2 = self.model.f2
        self.failure_rate3 = self.model.f3
        self.failure_rate4 = self.model.f4
        self.failure_rate5 = self.model.f5
        self.failure_rateother = self.model.fo

        # using time counting, in hours
        self.usingtime1 = 0
        self.usingtime2 = 0
        self.usingtime3 = 0
        self.usingtime4 = 0 
        self.usingtime5 = 0
        self.usingtimeo = 0

        self.Cum_failtime1 = 0
        self.Cum_failtime2 = 0
        self.Cum_failtime3 = 0
        self.Cum_failtime4 = 0 
        self.Cum_failtime5 = 0
        self.Cum_failtimeo = 0

        # fail probability
        self.Pf1 = 0
        self.pf2 = 0
        self.pf3 = 0
        self.pf4 = 0
        self.pf5 = 0
        self.pfo = 0

        self.P1 = random.random()
        self.P2 = random.random()
        self.P3 = random.random()
        self.P4 = random.random()
        self.P5 = random.random()
        self.Po = random.random()

        self.spareparts_usenumber_count = 0      
    
    def time_counting(self):
        # When the physical asset is working, the using time will +1 for each step
        # The using time will affect the failure probability
        if self.is_working == True:
            if self.component1_fail == False:
                self.usingtime1 += 1

            if self.component2_fail == False:
                self.usingtime2 += 1        

            if self.component3_fail == False:
                self.usingtime3 += 1   

            if self.component4_fail == False:
                self.usingtime4 += 1

            if self.component5_fail == False:
                self.usingtime5 += 1

            if self.componentother_fail == False:
                self.usingtimeo += 1
        
        
        if self.is_working == False:
            if self.component1_fail == True:
                self.usingtime1 = 0
                self.Cum_failtime1 += 1
            
            if self.component2_fail == True:
                self.usingtime2 = 0
                self.Cum_failtime2 += 1

            if self.component3_fail == True:
                self.usingtime3 = 0
                self.Cum_failtime3 += 1

            if self.component4_fail == True:
                self.usingtime4 = 0
                self.Cum_failtime4 += 1

            if self.component5_fail == True:
                self.usingtime5 = 0
                self.Cum_failtime5 += 1

            if self.componentother_fail == True:
                self.usingtimeo = 0
                self.Cum_failtimeo += 1

        

              
    def machine_working(self):
        # Aussume all the component are in a series structure
        # If any one is fail, the physical is down.
        # Once it fails, the time to repair will be recorded.
        if self.component1_fail == True or self.component2_fail == True \
            or self.component3_fail == True or self.component4_fail == True \
                or self.component5_fail == True or self.componentother_fail == True:
            self.is_working = False
            self.TTR += 1

        # When all the component is in good condition, the physical asset is in good condition.
        # Besides, when the shceduled maintenance is under going, it is also down.
        if self.component1_fail == False and self.component2_fail == False \
            and self.component3_fail == False and self.component4_fail == False \
                and self.component5_fail == False and self.componentother_fail == False:
            self.is_working = True
            self.no_fail += 1
            for agent in self.model.schedule.agents:
                if isinstance(agent, Maintenance_crew) and agent.doing_scheduled_maintenance == True:
                    self.is_working = False
        
    def machine_working_hour_count(self):
        if self.is_working == True:
            self.working_hours +=1
        
    def component_fail(self):
        #assume it is exponential distribution, Reliability = 1 - F
        self.pf1 = 1-math.exp(-self.failure_rate1* self.usingtime1)
        self.pf2 = 1-math.exp(-self.failure_rate2* self.usingtime2)
        self.pf3 = 1-math.exp(-self.failure_rate3* self.usingtime3)
        self.pf4 = 1-math.exp(-self.failure_rate4* self.usingtime4)
        self.pf5 = 1-math.exp(-self.failure_rate5* self.usingtime5)
        self.pfo = 1-math.exp(-self.failure_rateother* self.usingtimeo)

        if self.is_working == True:
            # We have the failure probability, using random function to determin its failure
            #It will be added to MTTF list for future calculation of The average MTTF.
            if self.P1<self.pf1:
                self.component1_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.P1 = random.random()
        
            if self.P2<self.pf2:
                self.component2_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.P2 = random.random()
        
            if self.P3<self.pf3:
                self.component3_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.P3 = random.random()
        
            if self.P4<self.pf4:
                self.component4_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.P4 = random.random()
        
            if self.P5<self.pf5:
                self.component5_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.P5 = random.random()

            if self.Po<self.pfo:
                self.componentother_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.spareparts_usenumber_count +=1
                self.Po = random.random()
            if (self.model.schedule.steps+1) % 365*8 == 0:
                self.spareparts_usenumber_count = 0
    
    def total_working_time_count(self):
        if self.is_working == True:
            self.total_working_time += 1 
      
  

    def step(self):
        self.component_fail()
        self.machine_working()
        self.machine_working_hour_count()
        self.time_counting()
        self.total_working_time_count()

         
# define warehouse agent
class Warehouse(Agent):
    """
    An agent representing warehouse in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        #Define the number of spare parts
        self.num_spareparts = self.model.num_spareparts
        self.sorting = self.model.sorting
        self.spare_parts_ready = False
    
    def sparepart_use(self):
        #Every time the number of spareparts will -1 if used
        if self.spare_parts_ready == True:
             self.num_spareparts -= 1
             if self.num_spareparts <= 0:
                 self.num_spareparts = 0
                 self.spare_parts_ready == False
  
    def get_spare_parts_ready(self):
        #Sorting need time
        for agent in self.model.schedule.agents:
            if isinstance(agent, Maintenance_crew) and agent.order_spare_parts == True and agent.sparepartsOK == False:
                self.sorting -= 1
                if self.sorting < 0:
                    self.sorting = 0

                if self.sorting ==0:
                    self.spare_parts_ready = True
                    self.sorting = self.model.sorting
    
    def step(self):
        self.get_spare_parts_ready()
        self.sparepart_use()

         


class Control_room(Agent):
    """
    An agent representing control room in manufacturing plant.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.warning = False
            
    def warning_display(self):
        #When physical Asset is failured, control room will display warning
        for agent in self.model.schedule.agents:
            if (isinstance(agent, PhysicalAsset) and agent.is_working == False): 
                self.warning = True
    
    
    def step(self):
        self.warning_display()


class Operation_crew(Agent):
    """
    An agent representing operation crew in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.upload_workorders = False

    def upload_work_orders(self):
        #If warning is displayed in the control room, operation crews will upload work orders.
        for agent in self.model.schedule.agents:
            if isinstance(agent, Control_room) and agent.warning == True:
              self.upload_workorders = True

    
    def step(self):
        self.upload_work_orders()

class Maintenance_crew(Agent):
    """
    An agent representing operation crew in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.case_open = False
        self.learning_time = self.model.learning_time
        self.repair_time = self.model.repair_time
        self.planning_time = self.model.planning_time
        self.is_failure_identified = False
        self.order_spare_parts = False
        self.chance_to_find_failure_in_schedule = self.model.chance_to_find_failure_in_schedule
        self.sparepartsOK = False
        self.doing_scheduled_maintenance = False
        self.maintenance_interval = self.model.maintenance_interval
        self.repairtime_scheduledmaintenance = self.model.repairtime_scheduledmaintenance

    
    def need_to_maintain(self):
        #When maintenance crews received the uploaded work orders, they will open the case
        for agent in self.model.schedule.agents:
            if isinstance(agent, SAP) and agent.create_workorders == True:
                self.case_open = True
                agent.create_workorders = False


    #check physical assets and learn
    def check_documentation_SPO(self):
        if self.case_open == True:
             self.learning_time -= 1
             if self.learning_time < 0:
                self.learning_time = 0

    def identify_failure(self):
        #Sometimes without the help of AI, failures cannot be identified, assume the rate to find the failure successfully is 0.9
        if self.learning_time == 0 and random.random() <self.chance_to_find_failure_in_schedule:
            self.is_failure_identified = True

                  
    def check_order_spare_parts(self):
        #When failure is identified, the needed spare parts will be ordered
        if self.is_failure_identified == True:
            self.order_spare_parts = True
        for agent in self.model.schedule.agents:
                if isinstance(agent, Warehouse) and agent.spare_parts_ready == True:
                    self.sparepartsOK = True
                    agent.spare_parts_ready = False

    
    def making_maintenance_plans(self):
        #When the failure is identified, the maintenance plans will be made
        if self.is_failure_identified == True:
             self.planning_time -= 1
             if self.planning_time < 0:
                self.planning_time = 0

             
    
    def repair(self):
    #When everything (spare parts, planning) is ready, do the repair. 
                if self.planning_time == 0 and self.sparepartsOK == True: 
                    self.repair_time -= 1
                    if self.repair_time < 0:
                        self.repair_time = 0
                    if self.repair_time == 0:
                        #Repair finished, case close. Reset the state of the machine.
                        self.case_open = False
                        for agent in self.model.schedule.agents:
                            if isinstance(agent, PhysicalAsset):
                                agent.component1_fail = False
                                agent.component2_fail = False
                                agent.component3_fail = False
                                agent.component4_fail = False
                                agent.component5_fail = False
                                agent.componentother_fail = False
                                if self.doing_scheduled_maintenance == False:
                                    if agent.TTR!=0:
                                        self.model.MTTR_list.append(agent.TTR)
                                        agent.TTR = 0
                            
                            if isinstance(agent, SAP):
                                agent.create_workorders = False

                            if isinstance(agent, Operation_crew):
                                agent.upload_workorders = False
                            
                            if isinstance(agent, Control_room):
                                agent.warning = False
                            

                        
                        self.sparepartsOK = False
                        self.is_failure_identified = False
                        self.order_spare_parts = False
                        self.repair_time = self.model.repair_time
                        self.planning_time = self.model.planning_time
                        self.learning_time = self.model.learning_time
             


    
    def scheduled_maintenance(self):
        # When the time reaches the maintenance interval, scheduled maintenance will be done.
        self.maintenance_interval -= 1
        
        if self.maintenance_interval <= 0:
            self.maintenance_interval = 0
        
        if self.maintenance_interval == 0:
            self.doing_scheduled_maintenance = True
        
        if self.doing_scheduled_maintenance == True:
            
            self.repairtime_scheduledmaintenance -= 1
            
            if self.repairtime_scheduledmaintenance <= 0:
                self.repairtime_scheduledmaintenance = 0
            
            if self.repairtime_scheduledmaintenance == 0:
                self.doing_scheduled_maintenance = False
                self.maintenance_interval = self.model.maintenance_interval
                self.repairtime_scheduledmaintenance = self.model.repairtime_scheduledmaintenance
                for agent in self.model.schedule.agents:
                    # Some will be reset, some will not, it is decided by the component situation
                    # However, it cannot be realized here in the code
                    # So I just use a random to determine this, there are 70% chance that the component will not be replaced.
                    if isinstance(agent, PhysicalAsset):
                        if agent.component1_fail == False and random.random() < 0.7:
                            agent.usingtime1 = 0
                            agent.spareparts_usenumber_count +=1
                            agent.P1=random.random()
                        if agent.component2_fail == False and random.random() < 0.7:
                            agent.usingtime2 = 0
                            agent.spareparts_usenumber_count +=1
                            agent.P2=random.random()
                        if agent.component3_fail == False and random.random() < 0.7:
                            agent.usingtime3 = 0
                            agent.spareparts_usenumber_count +=1
                            agent.P3=random.random()
                        if agent.component4_fail == False and random.random() < 0.7:
                            agent.usingtime4 = 0
                            agent.spareparts_usenumber_count +=1
                            agent.P4=random.random()
                        if agent.component5_fail == False and random.random() < 0.7:
                            agent.usingtime5 = 0
                            agent.spareparts_usenumber_count +=1
                            agent.P5=random.random()
                        #other parts will not be scheduled maintained because they are non-critical
   

    def step(self):
        self.need_to_maintain()
        self.check_documentation_SPO()
        self.identify_failure()
        self.check_order_spare_parts()
        self.making_maintenance_plans()
        self.repair()
        self.scheduled_maintenance()
        



class SAP(Agent):
    """
    An agent representing operation crew in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.create_workorders = False
    
    def create_work (self):
        #Here is where the work order is uploaded, it is the communication technology between Operation and maintenance crews
        for agent in self.model.schedule.agents:
                if isinstance(agent, Operation_crew) and agent.upload_workorders == True:
                    self.create_workorders = True

    
    def step(self):
        self.create_work()


#class SPO(Agent): No need to be seperated defined here

class equipment_supplier(Agent):
    """
    An agent representing operation crew in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.ready_to_deliver = False
        self.lead_time = self.model.lead_time

    def achieve_orders(self):
        # When the number of spare parts <=5, order them from equipment supplier
        for agent in self.model.schedule.agents:
            if isinstance(agent, Warehouse) and agent.num_spareparts <= 0.5*self.model.num_spareparts :
                self.ready_to_deliver = True

    
    def delivery(self):
        if self.ready_to_deliver == True:
             self.lead_time -= 1
             if self.lead_time < 0:
                 self.lead_time = 0
             if self.lead_time  == 0:
                # When it is delivered, the number of spare parts in Warehouse will return to 10
                for agent in self.model.schedule.agents:
                    if isinstance(agent, Warehouse):
                        agent.num_spareparts = self.model.num_spareparts
                        self.ready_to_deliver = False
                        self.lead_time = self.model.lead_time
    
    def step(self):
        self.achieve_orders()
        self.delivery()