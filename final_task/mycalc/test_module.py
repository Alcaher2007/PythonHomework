from mycalc.pythoncalc import calc
import unittest
from math import *
import mycalc.my_module


class TestCalculator(unittest.TestCase):

    def test_unar(self):
        self.assertEqual(calc('--+--2'), --+--2)
        self.assertEqual(calc('-2'), -2)
        self.assertEqual(calc('--------1'), 1)
        self.assertEqual(calc('-++--23+-++-3'), -20)
        self.assertEqual(calc('--.3-.3'), 0)
        self.assertEqual(calc('6-(-13)'), 19)
        self.assertEqual(calc('.6-+-(--13)'), 13.6)
        self.assertEqual(calc('++--2'), 2)
        self.assertEqual(calc('-2*2^3*-2'), -2*2**3*-2)
        self.assertEqual(calc('1---1'), 1---1)

    def test_comparison(self):
        self.assertFalse(calc('3+2/3==3+1'))
        self.assertFalse(calc('1<3<1'))
        self.assertFalse(calc('1>=0!=0'))
        self.assertFalse(calc('pi+1^0!=pi+1^250'))
        self.assertTrue(calc('pi+1^0==pi+1^250'))
        self.assertTrue(calc('1^256==1^0'))
        self.assertTrue(calc('1!=3<5'))

    def test_associative(self):
        self.assertEqual(calc('2^3^4'), 2**3**4)
        self.assertEqual(calc('2*2*2*3'), 2*2*2*3)
        self.assertEqual(calc('2/3/1'), 2/3/1)

    def test_consts_and_func(self):
        self.assertEqual(calc('pi+pi'), pi+pi)
        self.assertEqual(calc('pow(pi,e)'), pow(pi, e))
        self.assertEqual(calc('log(e)'), log(e))
        self.assertEqual(calc('log(e,e)'), log(e, e))
        self.assertEqual(calc('round(123.123)'), round(123.123))
        self.assertEqual(calc('round(123.123, 1)'), round(123.123, 1))
        self.assertEqual(calc('acos(256^0)*sin(3^0)'), acos(256**0)*sin(3**0))
        self.assertEqual(calc('2*sin(pi/2)'), 2*sin(pi/2))
        self.assertEqual(calc('factorial(11)'), factorial(11))
        self.assertEqual(calc('frexp(e)'), frexp(e))
        self.assertEqual(calc('trunc(123.123)'), trunc(123.123))
        self.assertEqual(calc('atan2(1,2)'), atan2(1, 2))

    def test_full(self):
        self.assertEqual(calc('(e^5-16.6-sin(1)/16.9)*123467'), (e**5-16.6-sin(1)/16.9)*123467)
        self.assertEqual(calc('-.2'), -0.2)
        self.assertEqual(calc('1337'), 1337)
        self.assertEqual(calc('2/2*sin(12^3)*.1+atan(0)'), 2/2*sin(12**3)*.1+atan(0))
        self.assertEqual(calc('(cos(e)^3+(2*3*acos(0)))'), (cos(e)**3+(2*3*acos(0))))
        self.assertEqual(calc('pow(sin(-cos(sin(0))), 0)'), pow(sin(-cos(sin(0))), 0))
        self.assertEqual(calc('+--e/-e+.1/.1--abs(-3)'), +--e/-e+.1/.1--abs(-3))
        self.assertEqual(calc('10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5'),
                         10*e**0*log10(.4-5 / -0.1-10) - -abs(-53/10) + -5)
        self.assertEqual(calc('sin(-cos(16)*2)--sin(-log(e))-cos(0)'), sin(-cos(16)*2)--sin(-log(e))-cos(0))
        self.assertEqual(calc('2.0^(2.0^2.0*2.0^2.0)'), 2.0**(2.0**2.0*2.0**2.0))
        self.assertEqual(calc('sin(pi/2^1) + log(1*4+2^2+1, 3^2)'),
                         sin(pi/2**1) + log(1*4+2**2+1, 3**2))
        self.assertEqual(calc('sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))'),
                         sin(e**log(e**e**sin(23.0), 45.0) + cos(3.0+log10(e**-e))))

    def test_errors(self):
        self.assertRaises(RuntimeError, calc, '')
        self.assertRaises(RuntimeError, calc, '((')
        self.assertRaises(RuntimeError, calc, '1+2*((3+2)')
        self.assertRaises(RuntimeError, calc, '==log(1)')
        self.assertRaises(RuntimeError, calc, '>1')
        self.assertRaises(RuntimeError, calc, '1>')
        self.assertRaises(RuntimeError, calc, 'log(e)/0')
        self.assertRaises(RuntimeError, calc, 'acos(1+1)')
        self.assertRaises(RuntimeError, calc, '1+3/4 7')
        self.assertRaises(RuntimeError, calc, '20 /* 6')
        self.assertRaises(RuntimeError, calc, '20/ /6/3+5')
        self.assertRaises(RuntimeError, calc, '-')
        self.assertRaises(RuntimeError, calc, '1+-1+')
        self.assertRaises(RuntimeError, calc, '123.123.4')
        self.assertRaises(RuntimeError, calc, '12.3+.123.5')
        self.assertRaises(RuntimeError, calc, '///////')
        self.assertRaises(RuntimeError, calc, 'round')
        self.assertRaises(RuntimeError, calc, 'abr(1)')
        self.assertRaises(RuntimeError, calc, '6 * * 6')
        self.assertRaises(RuntimeError, calc, 'pow(2, 3, 4)')
        self.assertRaises(RuntimeError, calc, '5 > = 6')

    def test_import_module(self):
        self.assertEqual(calc('pi', ['mycalc.my_module']), mycalc.my_module.pi)
        self.assertEqual(calc('acos(100)', ['mycalc.my_module']), mycalc.my_module.acos(100))
        self.assertEqual(calc('cos(1,3)', ['mycalc.my_module']), mycalc.my_module.cos(1, 3))
        self.assertEqual(calc('sin(17)', ['mycalc.my_module']), mycalc.my_module.sin(17))
        self.assertEqual(calc('factorial(0)', ['mycalc.my_module']), mycalc.my_module.factorial(0))
