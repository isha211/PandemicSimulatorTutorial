from ..interfaces import PersonState, Person

__all__ = ['VaccProgram']

class VaccProgram:
    num_vaccines_per_day: int
    vaxx_start_day: int
    days_between_doses: int
    num_retired_vaccinated:int
    num_adult_vaccinated:int

    def __init__(self, num_old_people, num_adult_people, num_minors):
        self.vaxx_start_day = 20
        self.days_between_doses = 7
        self.num_old_people = num_old_people
        self.num_adult_people = num_adult_people
        self.num_minors = num_minors
        self.num_retired_vaccinated = 0
        self.num_adult_vaccinated = 0

    def vacc_eligible(self, person: Person, current_day: int, num_vaccines_left: int) -> bool:
        if num_vaccines_left==0:
            return False
        if person.state.anti_vaxxer:
            return False
        if (person.state.vaccination_state==0
            or current_day > person.state.last_vaccinated_day + self.days_between_doses) \
            and current_day >= self.vaxx_start_day:
            if (person.id.age> 65 or person.state.risk == "HIGH"):
                return True

            if person.id.age<=65 and person.id.age>18:
                if (person.state.vaccination_state==0
                    and self.num_retired_vaccinated/self.num_old_people >=0.2) \
                        or person.state.vaccination_state>=1:
                    return True

            if person.id.age<18:
                if (person.state.vaccination_state==0
                    and self.num_adult_vaccinated/self.num_adult_people>=0.2) \
                        or person.state.vaccination_state>=1:
                    return True

        return False
        # if vacc_stage == 1:
        #     if person.id.age>=60 or person.state.risk == "HIGH": #40
        #         print("Stage 1 +1 vaccinated")
        #         return True
        #
        # if vacc_stage == 2:
        #     if person.id.age>=45 or person.state.risk == "HIGH": #40
        #         print("Stage 2 +1 vaccinated")
        #         return True
        #
        # if vacc_stage == 3:
        #     if person.id.age>=18 or person.state.risk == "HIGH": #40
        #         print("Stage 3 +1 vaccinated")
        #         return True
        #
        # return False




    def vacc_person(self, person: Person, current_day: int):
        if person.state.vaccination_state<3:
            if person.state.vaccination_state == 0:
                if person.id.age > 65:
                    self.num_retired_vaccinated += 1
                elif person.id.age <= 65 and person.id.age>18:
                    self.num_adult_vaccinated += 1
            person.state.vaccination_state = person.state.vaccination_state + 1
            # person.state.infection_spread_multiplier *= (1 - person.state.vaccination_state*self.vaccine_efficacy)
            person.state.infection_state.spread_probability *= 0.5
            person.state.last_vaccinated_day = current_day
            return True
        return False