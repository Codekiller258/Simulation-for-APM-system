# import necessary libraries
import math
import random
from mesa import Agent
import numpy as np

# define PhysicalAsset agent
class PhysicalAssetAI(Agent):
    """
    An agent representing physical asset in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
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

        # assign failure rates, in hours
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
        self.spareparts_use_counting = 0
    
    def time_counting(self):
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
                self.usingtimeo+= 1
        
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

    
    def machine_working_hour_count(self):
        if self.is_working == True:
            self.working_hours +=1
    
    def machine_working(self):
        # Assume it is a series structure.
        # One component fails, the machine fails
        if self.component1_fail == True or self.component2_fail == True or self.component3_fail == True or self.component4_fail == True or self.component5_fail == True or self.componentother_fail == True:
            self.is_working = False
            self.TTR += 1
        # Machine only works when all the components works. 
        if self.component1_fail == False and self.component2_fail == False and self.component3_fail == False and self.component4_fail == False and self.component5_fail == False and self.componentother_fail == False:
            self.is_working = True
            self.no_fail += 1

    def component_fail(self):
        #assume it is exponential distribution, Reliability = 1 - F
        self.pf1 = 1-math.exp(-self.failure_rate1* self.usingtime1)
        self.pf2 = 1-math.exp(-self.failure_rate2* self.usingtime2)
        self.pf3 = 1-math.exp(-self.failure_rate3* self.usingtime3)
        self.pf4 = 1-math.exp(-self.failure_rate4* self.usingtime4)
        self.pf5 = 1-math.exp(-self.failure_rate5* self.usingtime5)
        self.pfo = 1-math.exp(-self.failure_rateother* self.usingtimeo)
        # We have the failure probability, using random function to determin its failure
        #It will be added to MTTF list for future calculation of The average MTTF.
        if self.is_working == True:
            if self.P1<self.pf1:
                self.component1_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.P1 = random.random()
        
            if self.P2<self.pf2:
                self.component2_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.P2 = random.random()
        
            if self.P3<self.pf3:
                self.component3_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.P3 = random.random()
        
            if self.P4<self.pf4:
                self.component4_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.P4 = random.random()
        
            if self.P5<self.pf5:
                self.component5_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.P5 = random.random()

            if self.Po<self.pfo:
                self.componentother_fail = True
                self.model.MTTF_list.append(self.no_fail)
                self.no_fail = 0
                self.Po = random.random()
            

    def total_working_time_count(self):
        if self.is_working == True:
            self.total_working_time += 1 
    
    def step(self):
        self.machine_working()
        self.component_fail()
        self.machine_working_hour_count()
        self.time_counting()
        self.total_working_time_count()

class WarehouseAI(Agent):
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.num_spareparts = self.model.num_spareparts
        self.sorting = self.model.sorting
        self.spare_parts_ready = False

    def get_spare_parts_ready(self):
        #Sorting need time
        for agent in self.model.schedule.agents:
            if isinstance(agent,UNS) and agent.inform_work == True and agent.sparepartsok == False:
                self. sorting -= 1
                if self.sorting ==0:
                    self.spare_parts_ready = True
                    self.sorting = self.model.sorting
    
    def spareparts_use(self):
        #Every time the number of spareparts will -1 if used
        if self.spare_parts_ready == True:
             self.num_spareparts -= 1
             if self.num_spareparts < 0:
                 self.num_spareparts = 0
                 self.spare_parts_ready = False
    def step(self):
        self.get_spare_parts_ready()
        self.spareparts_use()



#class OperationAI(Agent):
#no need to do anything now, because it is not needed in this system boundary

class MaintenanceAI(Agent):
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        
        self.case_open = False
       
        self.learning_time1 = self.model.learning_time
        self.learning_time2 = self.model.learning_time
        self.learning_time3 = self.model.learning_time
        self.learning_time4 = self.model.learning_time
        self.learning_time5 = self.model.learning_time
        self.learning_timeo = self.model.learning_time
        
        self.repair_time1 = self.model.repair_time
        self.repair_time2 = self.model.repair_time
        self.repair_time3 = self.model.repair_time
        self.repair_time4 = self.model.repair_time
        self.repair_time5 = self.model.repair_time
        self.repair_timeo = self.model.repair_time
        
        self.planning_time1 = self.model.planning_time
        self.planning_time2 = self.model.planning_time
        self.planning_time3 = self.model.planning_time
        self.planning_time4 = self.model.planning_time
        self.planning_time5 = self.model.planning_time
        self.planning_timeo = self.model.planning_time

        self.plansok1 = False
        self.plansok2 = False
        self.plansok3 = False
        self.plansok4 = False
        self.plansok5 = False
        self.plansoko = False
        
        self.is_failure_identified1 = False
        self.is_failure_identified2 = False
        self.is_failure_identified3 = False
        self.is_failure_identified4 = False
        self.is_failure_identified5 = False
        self.is_failure_identifiedo = False
        
        self.sparepartsOK = False


    def opencase(self):
        #When UNS inform work, the case will open
        for agent in self.model.schedule.agents:
            if isinstance(agent, UNS) and agent.inform_work == True:
                self.case_open = True
    
    def learning_failure(self):
        # Maintenance crews learn to identify failures
        # Different components are seperately presented due to the AI. Because AI can distinguish which one is wrong.
        if self.case_open == True:
            for agent in self.model.schedule.agents:
                if isinstance(agent, UNS):
                    if agent.abnormal_signals1 == False:
                        # AI make the system into a wisdom level, so the learning time reduced according to
                        # the wisdom level of AI and historical data level.
                        self.learning_time1 = self.model.learning_time*(1-( 0.1*agent.historical_data1 + agent.wisdom_level))
                    if agent.abnormal_signals1 == True:
                        self.learning_time1 -= 1
                        if self.learning_time1 <= 0:
                            self.is_failure_identified1 = True

                    if agent.abnormal_signals2 == False:
                        self.learning_time2 = self.model.learning_time*(1-( 0.1*agent.historical_data2 + agent.wisdom_level))
                    if agent.abnormal_signals2 == True:
                        self.learning_time2 -= 1
                        if self.learning_time2 <= 0:
                            self.is_failure_identified2 = True

                    if agent.abnormal_signals3 == False:
                        self.learning_time3 = self.model.learning_time*(1-( 0.1*agent.historical_data3 + agent.wisdom_level))
                    if agent.abnormal_signals3 == True:
                        self.learning_time3 -= 1
                        if self.learning_time3 <= 0:
                            self.is_failure_identified3 = True

                    if agent.abnormal_signals4 == False:
                        self.learning_time4 = self.model.learning_time*(1-( 0.1*agent.historical_data4 + agent.wisdom_level))
                    if agent.abnormal_signals4 == True:
                        self.learning_time4 -= 1
                        if self.learning_time4 <= 0:
                            self.is_failure_identified4 = True

                    if agent.abnormal_signals5 == False:
                        self.learning_time5 = self.model.learning_time*(1-( 0.1*agent.historical_data5 + agent.wisdom_level))
                    if agent.abnormal_signals5 == True:
                        self.learning_time5 -= 1
                        if self.learning_time5 <= 0:
                            self.is_failure_identified5 = True

                    if agent.abnormal_signalso == False:
                        self.learning_timeo = self.model.learning_time*(1-0.1*agent.historical_datao)
                    if agent.abnormal_signalso == True:
                        self.learning_timeo -= 1
                        if self.learning_timeo <= 0:
                            self.is_failure_identifiedo = True
    
    def planning(self):
        # When the failure is identified successfully.
        for agent in self.model.schedule.agents:
            if isinstance(agent, UNS):
                # AI make the system into a wisdom level, it can help with the maintenance plan
                # so the planning time reduced according to
                # the wisdom level of AI and historical data level.
                if agent.abnormal_signals1 == False:
                    self.planning_time1 = self.model.planning_time*(1-( 0.1*agent.historical_data1 + agent.wisdom_level))
                if self.is_failure_identified1 == True:
                    self.planning_time1 -= 1
                    if self.planning_time1 <=0:
                        self.plansok1 = True

                if agent.abnormal_signals2 == False:
                    self.planning_time2 = self.model.planning_time*(1-( 0.1*agent.historical_data2 + agent.wisdom_level))
                if self.is_failure_identified2 == True:
                    self.planning_time2 -= 1
                    if self.planning_time2 <=0:
                        self.plansok2 = True
                
                if agent.abnormal_signals3 == False:
                    self.planning_time3 = self.model.planning_time*(1-( 0.1*agent.historical_data3 + agent.wisdom_level))
                if self.is_failure_identified3 == True:
                    self.planning_time3 -= 1
                    if self.planning_time3 <=0:
                        self.plansok3 = True

                if agent.abnormal_signals4 == False:
                    self.planning_time4 = self.model.planning_time*(1-( 0.1*agent.historical_data4 + agent.wisdom_level))
                if self.is_failure_identified4 == True:
                    self.planning_time4 -= 1
                    if self.planning_time4 <=0:
                        self.plansok4 = True

                if agent.abnormal_signals5 == False:
                    self.planning_time5 = self.model.planning_time*(1-( 0.1*agent.historical_data5 + agent.wisdom_level))
                if self.is_failure_identified5 == True:
                    self.planning_time5 -= 1
                    if self.planning_time5 <=0:
                        self.plansok5 = True

                if agent.abnormal_signalso == False:
                    self.planning_timeo = self.model.planning_time*(1 - 0.1*agent.historical_datao)
                if self.is_failure_identifiedo == True:
                    self.planning_timeo -= 1
                    if self.planning_timeo <=0:
                        self.plansoko = True
    
    def check_spareparts(self):
        # Check whether spare parts is prepared by warehouse
        for agent in self.model.schedule.agents:
            if isinstance(agent, UNS) and agent.sparepartsok == True:
                self.sparepartsOK = True

    def doing_maintenance(self):
        #When plans are ok, and spareparts are ok, maintenance starts
        if self.plansok1 == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    # When the maintenance starts, the machine will be turned down.
                    agent.is_working = False
                    self.repair_time1 -= 1
                    if self.repair_time1 <= 0:
                        agent.usingtime1 = 0
                        agent.spareparts_use_counting += 1
                        if agent.component1_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0

                        # When the maintenance is finished, the component state will be reset
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signals1 = False
                                agent.component1_fail = False
                                agent.P1 = random.random()
                                self.is_failure_identified1 = False
                                self.learning_time1 = self.model.learning_time*(1-( 0.1*U.historical_data1 + U.wisdom_level))
                                self.planning_time1 = self.model.planning_time*(1-( 0.1*U.historical_data1 + U.wisdom_level))
                                self.plansok1 = False
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                # Every time the maintenance is finished, historical data will add 1
                                U.historical_data1 += 1
                                #print('1 accumulate historical data',U.historical_data1)
                                if U.historical_data1 >= (1-U.wisdom_level)*10:
                                    U.historical_data1 = (1-U.wisdom_level)*10
                                self.repair_time1 = self.model.repair_time*(1-0.1*U.historical_data1)

        if self.plansok2 == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    agent.is_working = False
                    self.repair_time2 -= 1
                    if self.repair_time2 <= 0:
                        agent.usingtime2 = 0
                        agent.spareparts_use_counting += 1
                        if agent.component2_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signals2 = False
                                agent.component2_fail = False
                                agent.P2 = random.random()
                                self.is_failure_identified2 = False
                                self.learning_time2 = self.model.learning_time*(1-( 0.1*U.historical_data2 + U.wisdom_level))
                                self.planning_time2 = self.model.planning_time*(1-( 0.1*U.historical_data2 + U.wisdom_level))
                                self.plansok2 = False
                                #self.repair_time2 = self.model.repair_time
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                U.historical_data2 += 1
                                if U.historical_data2 >= (1-U.wisdom_level)*10:
                                    U.historical_data2 = (1-U.wisdom_level)*10
                                self.repair_time2 = self.model.repair_time*(1-0.1*U.historical_data2)

        if self.plansok3 == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    agent.is_working = False
                    self.repair_time3 -= 1
                    if self.repair_time3 <= 0:
                        agent.usingtime3 = 0
                        agent.spareparts_use_counting += 1
                        if agent.component3_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signals3 = False
                                agent.component3_fail = False
                                agent.P3 = random.random()
                                self.is_failure_identified3 = False
                                self.learning_time3 = self.model.learning_time*(1-( 0.1*U.historical_data3 + U.wisdom_level))
                                self.planning_time3 = self.model.planning_time*(1-( 0.1*U.historical_data3 + U.wisdom_level))
                                self.plansok3 = False
                                #self.repair_time3 = self.model.repair_time
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                U.historical_data3 += 1
                                if U.historical_data3 >= (1-U.wisdom_level)*10:
                                    U.historical_data3 = (1-U.wisdom_level)*10
                                self.repair_time3 = self.model.repair_time*(1-0.1*U.historical_data3)
        
        if self.plansok4 == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    agent.is_working = False
                    self.repair_time4 -= 1
                    if self.repair_time4 <= 0:
                        agent.usingtime4 = 0
                        agent.spareparts_use_counting += 1
                        if agent.component5_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signals4 = False
                                agent.component4_fail = False
                                agent.P4 = random.random()
                                self.is_failure_identified4 = False
                                self.learning_time4 = self.model.learning_time*(1-( 0.1*U.historical_data4 + U.wisdom_level))
                                self.planning_time4 = self.model.planning_time*(1-( 0.1*U.historical_data4 + U.wisdom_level))
                                self.plansok4 = False
                                #self.repair_time4 = self.model.repair_time
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                U.historical_data4 += 1
                                if U.historical_data4 >= (1-U.wisdom_level)*10:
                                    U.historical_data4 = (1-U.wisdom_level)*10
                                self.repair_time4 = self.model.repair_time*(1-0.1*U.historical_data4)

        if self.plansok5 == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    agent.is_working = False
                    self.repair_time5 -= 1
                    if self.repair_time5 <= 0:
                        agent.usingtime5 = 0
                        agent.spareparts_use_counting += 1
                        if agent.component5_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signals5 = False
                                agent.component5_fail = False
                                agent.P5 = random.random()
                                self.is_failure_identified5 = False
                                self.learning_time5 = self.model.learning_time*(1-( 0.1*U.historical_data5 + U.wisdom_level))
                                self.planning_time5 = self.model.planning_time*(1-( 0.1*U.historical_data5 + U.wisdom_level))
                                self.plansok5 = False
                                #self.repair_time5 = self.model.repair_time
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                U.historical_data5 += 1
                                if U.historical_data5 >= (1-U.wisdom_level)*10:
                                    U.historical_data5 = (1-U.wisdom_level)*10
                                self.repair_time5 = self.model.repair_time*(1-0.1*U.historical_data5)
        
        if self.plansoko == True and self.sparepartsOK == True:
            for agent in self.model.schedule.agents:
                if isinstance (agent, PhysicalAssetAI):
                    agent.is_working = False
                    self.repair_timeo -= 1
                    if self.repair_timeo <= 0:
                        agent.usingtimeo = 0
                        agent.spareparts_use_counting += 1
                        if agent.componentother_fail == True:
                            if agent.TTR !=0:
                                self.model.MTTR_list.append(agent.TTR)
                                agent.TTR = 0
                        for U in self.model.schedule.agents:
                            if isinstance(U,UNS):
                                U.abnormal_signalso = False
                                agent.componentother_fail = False
                                agent.Po = random.random()
                                self.is_failure_identifiedo = False
                                self.learning_timeo = self.model.learning_time*(1-( 0.1*U.historical_datao ))
                                self.planning_timeo = self.model.planning_time*(1-( 0.1*U.historical_datao ))
                                self.plansoko = False
                                self.sparepartsOK = False
                                U.sparepartsok = False
                                U.historical_datao += 1
                                if U.historical_datao >= (1-U.wisdom_level)*10:
                                    U.historical_datao = (1-U.wisdom_level)*10
                                self.repair_timeo = self.model.repair_time*(1-0.1*U.historical_datao)

    def close_case(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent,UNS) and agent.inform_work == False:
                self.open_case = False
    
    def step(self):
        self.opencase()
        self.learning_failure()
        self.planning()
        self.check_spareparts()
        self.doing_maintenance()
        self.close_case()

  


class UNS(Agent):
    """
    An agent representing UNS in the whole business process.
    """
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)

        
        #the original wisdom level of AI
        self.wisdom_level = self.model.wisdom_level
        
        #historical data collected from previous failures, 
        #every successful repair will add 1 unit of historical data
        self.historical_data1 = 0
        self.historical_data2 = 0
        self.historical_data3 = 0
        self.historical_data4 = 0
        self.historical_data5 = 0
        self.historical_datao = 0

        #failure signal detected
        self.abnormal_signals1 = False
        self.abnormal_signals2 = False
        self.abnormal_signals3 = False
        self.abnormal_signals4 = False
        self.abnormal_signals5 = False
        self.abnormal_signalso = False

        self.inform_work = False
        self.sparepartsok = False



    def failure_detection (self):
        #it will be better to model with real signal and failure threshold, but I don't have the conditions
        for agent in self.model.schedule.agents:
            if isinstance (agent,PhysicalAssetAI):
                # IF the using time reaches 60% of the expected component life, it will be detected.
                if agent.usingtime1 >= 0.6*math.log(1-agent.P1)/(-agent.failure_rate1) \
                    or agent.component1_fail == True:
                    self.abnormal_signals1 = True
                
                if agent.usingtime2 >= 0.6*math.log(1-agent.P2)/(-agent.failure_rate2) \
                    or agent.component2_fail == True:
                    self.abnormal_signals2 = True
                
                if agent.usingtime3 >= 0.6*math.log(1-agent.P3)/(-agent.failure_rate3) \
                    or agent.component3_fail == True:
                    self.abnormal_signals3 = True

                if agent.usingtime4 >= 0.6*math.log(1-agent.P4)/(-agent.failure_rate4) \
                    or agent.component4_fail == True:
                    self.abnormal_signals4 = True

                if agent.usingtime5 >= 0.6*math.log(1-agent.P5)/(-agent.failure_rate5) \
                    or agent.component5_fail == True:
                    self.abnormal_signals5 = True
                
                if   agent.componentother_fail == True:
                    self.abnormal_signalso = True
            
            if self.abnormal_signals1 == True or self.abnormal_signals2 == True \
                or self.abnormal_signals3 == True or self.abnormal_signals4 == True \
                    or self.abnormal_signals5 == True or self.abnormal_signalso == True:
                self.inform_work = True

    def spareparts_states(self):
        # IF warehouse already get the spare parts ready, they will inform this on UNS
        for agent in self.model.schedule.agents:
                if isinstance(agent, WarehouseAI) and agent.spare_parts_ready == True:
                    self.sparepartsok = True
                    agent.spare_parts_ready = False
    
    def being_normal(self):
        if self.abnormal_signals1 == False and self.abnormal_signals2 == False and self.abnormal_signals3 == False and self.abnormal_signals4 == False and self.abnormal_signals5 == False and self.abnormal_signalso == False:
            self.inform_work = False

    def step(self):
        self.failure_detection()
        self.spareparts_states()
        self.being_normal()
            
class EquipmentAI(Agent):
    def __init__(self, unique_id, model,seed):
        super().__init__(unique_id, model)
        self.ready_to_deliver = False
        self.lead_time = self.model.lead_time

    def achieve_orders(self):
        #If there are less than 5 spareparts in warehouse, the order will be done by UNS.
        for agent in self.model.schedule.agents:
            if isinstance(agent, WarehouseAI) and agent.num_spareparts <= 0.5*self.model.num_spareparts :
                self.ready_to_deliver = True

    def delivery(self):
        if self.ready_to_deliver == True:
             self.lead_time -= 2
             if self.lead_time < 0:
                 self.lead_time = 0
             if self.lead_time  == 0:
                for agent in self.model.schedule.agents:
                    if isinstance(agent, WarehouseAI):
                        agent.num_spareparts = self.model.num_spareparts
                        self.ready_to_deliver = False
                        self.lead_time = self.model.lead_time
    
    def step(self):
        self.achieve_orders()
        self.delivery()