#!/usr/bin/python3


import sys
import constraint
import typing


def main():

        l2 = sys.argv[2][1:-1].split(",")

        parse_2 = list(map(int, l2))

        try:
                
                l3 = sys.argv[3][1:-1].split(",")

                parse_3 = list(map(int, l3))

        except: parse_3 = []
        
        people = ['claude', 'olga', 'pablo', 'scott']

        times = ['2:30', '3:30', '4:30', '5:30']

        dests = ['peru', 'romania', 'taiwan', 'yemen']

        p = setup_problem(people, times, dests)

        print(p)

        if 1 in parse_2:
                p = ax_1(p, people)

        if 2 in parse_2:
                p = ax_2(p, people)

        if 3 in parse_2:
                p = ax_3(p, people)

        if 4 in parse_2:
                p = ax_4(p, people)

        if 5 in parse_2:
                p = ax_5(p, people)

        print(p.getSolutions())


def ax_1(p: constraint.problem.Problem, people: list[str]) -> constraint.problem.Problem:

        ##  Sample instance of domain overlaid to variables, after
        ##  applying constraint:
        
        ##  { 't_olga': '3:30', 
       ##    'd_olga': 'taiwan',
        ##    'd_claude': 'peru',
        ##    'd_pablo': 'yemen',
        ##    'd_scott': 'romania',
        ##    't_pablo': '5:30',
        ##    't_claude': '4:30',
        ##    't_scott': '2:30' }

        ##  addConstaint will take a set of variables and conditions
        ##  and return true/false based on whether to consider it as a
        ##  valid constraint.

        ##  As a result, sets of variables will be filtered away from
        ##  the solutions.

        for person in people:

                p.addConstraint(
                        
                        (lambda x, y, z:

                        ##  If the destination of the person is not
                        ##  Yemen.
                        
                        (y != 'yemen')

                        ##  Then the instance of variables satisfies
                        ##  the constraint.

                        ##  However if it is Yemen, and the person's
                        ##  timing is 2 hours later than Olga...
                        
                        or ((x == '4:30') and (z == '2:30'))
                        
                        or ((x == '5:30') and (z == '3:30'))

                        ##  Then the instance of variables satisfies
                        ##  the constraint.
                        
                        ),

                ##  't_claude': '5:30'
                ##  'd_claude': 'yemen'
                ##  't_olga':   '3:30'
                ##  The above would evaluate to true.

                ##  't_olga':   '5:30'
                ##  'd_olga':   'yemen'
                ##  't_olga':   '3:30'
                ##  The above would evalute to false, presumably,
                ##  given a variable cannot take 2 values.

                ['t_'+person, 'd_'+person, 't_olga']

                )
                
        return p


def ax_2(p: constraint.problem.Problem, people: list[str]) -> constraint.problem.Problem:
        
        p.addConstraint(

                (lambda x:
                
                (x == '2:30') or (x == '3:30')
                        
                ),

                ['t_claude']

        )
                
        return p
        

def ax_3(p: constraint.problem.Problem, people: list[str]) -> constraint.problem.Problem:
        
        for person in people:

                p.addConstraint(

                        (lambda x, y:

                         ((x == '2:30') and (y == 'peru'))

                         or ( x != '2:30')
                 
                        ),

                        ['t_'+person, 'd_'+person]

                )
                
        return p
        

def ax_4(p: constraint.problem.Problem, people: list[str]) -> constraint.problem.Problem:

        for person in people:

                people_subset = people[:]

                people_subset.remove(person)

                for person2 in people_subset:

                        p.addConstraint(

                                (lambda t, t2, d, d2:
                
                                ((d == 'yemen') and (d2 == 'taiwan') and int(t[0]) < int(t2[0]))

                                or (d != 'yemen')
                        
                                ),

                                ['t_'+person, 't_'+person2, 'd_'+person, 'd_'+person2]

                        )
                
        return p
        

def setup_problem(people: list[str], times: list[str], destinations: list[str]) -> constraint.problem.Problem:
        
        problem = constraint.Problem()

        t_variables = list(map(( lambda x: 't_'+x ), people))

        d_variables = list(map(( lambda x: 'd_'+x ), people))

        print(t_variables)

        print(d_variables)

        problem.addVariables(t_variables, times)

        problem.addVariables(d_variables, destinations)

        # no two travellers depart at the same time

        problem.addConstraint(constraint.AllDifferentConstraint(), t_variables)

        # no two travellers return from the same destination

        problem.addConstraint(constraint.AllDifferentConstraint(), d_variables)
        
        return problem


main()
