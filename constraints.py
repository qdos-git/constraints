#!/usr/bin/python3


import sys
import constraint
import typing


def main():

        l2 = sys.argv[2][1:-1].split(",")

        parse_2 = list(map(int, l2))

        l3 = sys.argv[3][1:-1].split(",")

        parse_3 = list(map(int, l3))
        
        people = ['claude', 'olga', 'pablo', 'scott']

        times = ['2:30', '3:30', '4:30', '5:30']

        dests = ['peru', 'romania', 'taiwan', 'yemen']

        p = setup_problem(people, times, dests)

        print(p)

        print("test")

        if 1 in parse_2:
                p = ax_1(p, people)

        print(len(p.getSolutions()))


def ax_1(p, people):

        for person in people:
                
                p.addConstraint((
                        
                        lambda x,y,z:
                        
                        (y != 'yemen')
                        
                        or ((x == '4:30') and (z == '2:30'))
                        
                        or ((x == '5:30') and (z == '3:30'))
                        
                ), ['t_'+person, 'd_'+person, 't_olga'])
                
        return p
                
        
def ax_1_alt(p, people):

        for person in people:
                
                p.addConstraint((
                        
                        lambda x,y,z:
                        
                        (y != 'yemen')
                        
                        or ((x == '4:30') and (z == '2:30'))
                        
                        or ((x == '5:30') and (z == '3:30'))
                        
                ), ['t_'+person, 'd_'+person, 't_olga'])
                
        return p
                
        
def setup_problem(people, times, destinations) -> constraint.problem.Problem:
        
        problem = constraint.Problem()

        t_variables= list(map(( lambda x: 't_'+x ), people))

        d_variables= list(map(( lambda x: 'd_'+x ), people))

        problem.addVariables(t_variables, times)

        problem.addVariables(d_variables, destinations)

        # no two travellers depart at the same time

        problem.addConstraint(constraint.AllDifferentConstraint(), t_variables)

        # no two travellers return from the same destination

        problem.addConstraint(constraint.AllDifferentConstraint(), d_variables)
        
        return problem


main()
