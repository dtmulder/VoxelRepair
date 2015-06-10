# -*- coding: utf-8 -*-
"""
Created on Thu May 07 22:25:38 2015

@author: Damien
"""
##############################################################################
# Imports
##############################################################################
import numpy as np


##############################################################################
# Lookup table
##############################################################################
# case number, number of tri's,  tri edge nodes (per 3)
lookup = {
'00000000':(0,0),
'11111111':(0,0),
'10000000':(1,1,9,4,1),	
'01000000':(1,1,1,2,10),
'00100000':(1,1,2,3,11),
'00010000':(1,1,4,12,3),
'00001000':(1,1,5,8,9),
'00000100':(1,1,10,6,5),
'00000010':(1,1,11,7,6),
'00000001':(1,1,7,12,8),
'01111111':(1,1,1,4,9),
'10111111':(1,1,10,2,1),
'11011111':(1,1,11,3,2),
'11101111':(1,1,3,12,4),
'11110111':(1,1,9,8,5),
'11111011':(1,1,5,6,10),
'11111101':(1,1,6,7,11),
'11111110':(1,1,8,12,7),
'11000000':(2,2,2,9,4,2,10,9),
'10010000':(2,2,12,1,9,3,1,12),
'10001000':(2,2,4,5,8,1,5,4),
'01100000':(2,2,10,3,11,1,3,10),	
'01000100':(2,2,6,1,2,5,1,6),	
'00110000':(2,2,4,11,2,12,11,4),
'00010001':(2,2,3,8,7,4,8,3),
'00100010':(2,2,7,2,3,7,6,2),
'00001100':(2,2,8,10,6,9,10,8),
'00001001':(2,2,7,9,5,12,9,7),
'00000110':(2,2,11,5,10,7,5,11),
'00000011':(2,2,12,6,11,8,6,12),  
'00111111':(2,2,2,4,9,2,9,10), 
'01101111':(2,2,12,9,1,3,12,1), 
'01110111':(2,2,4,8,5,1,4,5), 
'10011111':(2,2,10,11,3,1,10,3), 
'10111011':(2,2,6,2,1,5,6,1), 
'11001111':(2,2,4,2,11,12,4,11), 
'11101110':(2,2,3,7,8,4,3,8), 
'11011101':(2,2,7,3,2,7,2,6),
'11110011':(2,2,8,6,10,9,8,10),
'11110110':(2,2,7,5,9,12,7,9), 
'11111001':(2,2,11,10,5,7,11,5), 
'11111100':(2,2,12,11,6,8,12,6), 
'10100000':(3,2,9,4,1,2,3,11),
'10000100':(3,2,9,4,1,10,6,5),
'10000001':(3,2,9,4,1,7,12,8),
'01010000':(3,2,1,2,10,4,12,3),
'01001000':(3,2,1,2,10,5,8,9),
'01000010':(3,2,1,2,10,11,7,6),
'00011000':(3,2,4,12,3,5,8,9),
'00010010':(3,2,4,12,3,11,7,6),
'00100100':(3,2,2,3,11,10,6,5),
'00100001':(3,2,2,3,11,7,12,8),
'00001010':(3,2,5,8,9,11,7,6),
'00000101':(3,2,10,6,5,7,12,8),
'01011111':(3,2,1,4,9,11,3,2),
'01111011':(3,2,1,4,9,5,6,10),
'01111110':(3,2,1,4,9,8,12,7),
'10101111':(3,2,10,2,1,3,12,4),
'10110111':(3,2,10,2,1,9,8,5),
'10111101':(3,2,10,2,1,6,7,11),
'11100111':(3,2,3,12,4,9,8,5),
'11101101':(3,2,3,12,4,6,7,11),
'11011011':(3,2,11,3,2,5,6,10),
'11011110':(3,2,11,3,2,8,12,7),
'11110101':(3,2,9,8,5,6,7,11),
'11111010':(3,2,5,6,10,8,12,7),
'10000010':(4,2,9,4,1,11,7,6),
'01000001':(4,2,1,2,10,7,12,8),
'00010100':(4,2,4,12,3,10,6,5),
'00101000':(4,2,2,3,11,5,8,9),
'01111101':(4,2,1,4,9,6,7,11),
'10111110':(4,2,10,2,1,8,12,7),
'11101011':(4,2,3,12,4,5,6,10),
'11010111':(4,2,11,3,2,9,8,5),
'11100000':(5,3,4,11,9,11,10,9,4,3,11),
'01110000':(5,3,1,12,10,12,11,10,1,4,12),
'10110000':(5,3,2,9,11,9,12,11,2,1,9),
'11010000':(5,3,12,3,10,10,9,12,3,2,10),
'01000110':(5,3,1,2,7,7,5,1,2,11,7),  
'00100110':(5,3,5,10,3,3,7,5,10,2,3),
'01100010':(5,3,7,6,1,1,3,7,6,10,1),
'01100100':(5,3,3,11,5,5,1,3,11,6,5),
'00001101':(5,3,10,6,12,12,9,10,6,7,12),
'00001011':(5,3,9,5,11,11,12,9,5,6,11),
'00000111':(5,3,12,8,10,10,11,12,8,5,10),
'00001110':(5,3,11,7,9,9,10,11,7,8,9),
'10011000':(5,3,5,8,3,3,1,5,8,12,3),
'10010001':(5,3,1,9,7,7,3,1,9,8,7),
'00011001':(5,3,3,4,5,5,7,3,4,9,5),
'10001001':(5,3,7,12,1,1,5,7,12,4,1),
'00110010':(5,3,4,12,6,6,2,4,12,7,6),
'00100011':(5,3,2,3,8,8,6,2,3,12,8),
'00010011':(5,3,6,11,4,4,8,6,11,3,4),
'00110001':(5,3,8,7,2,2,4,8,7,11,2),
'01001100':(5,3,8,9,2,2,6,8,9,1,2),
'11000100':(5,3,6,5,4,4,2,6,5,9,4),
'11001000':(5,3,2,10,8,8,4,2,10,5,8),
'10001100':(5,3,4,1,6,6,8,4,1,10,6),
'00011111':(5,3,4,9,11,11,9,10,4,11,3),
'10001111':(5,3,1,10,12,12,10,11,1,12,4),
'01001111':(5,3,2,11,9,11,12,9,2,9,1),
'00101111':(5,3,12,10,3,10,12,9,3,10,2),
'10111001':(5,3,1,7,2,7,1,5,2,7,11),
'11011001':(5,3,5,3,10,3,5,7,10,3,2),
'10011101':(5,3,7,1,6,1,7,3,6,1,10),
'10011011':(5,3,3,5,11,5,3,1,11,5,6),
'11110010':(5,3,10,12,6,12,10,9,6,12,7),
'11110100':(5,3,9,11,5,11,9,12,5,11,6),
'11111000':(5,3,12,10,8,10,12,11,8,10,5),
'11110001':(5,3,11,9,7,9,11,10,7,9,8),
'01100111':(5,3,5,3,8,3,5,1,8,3,12),
'01101110':(5,3,1,7,9,7,1,3,9,7,8),
'11100110':(5,3,3,5,4,5,3,7,4,5,9),
'01110110':(5,3,7,1,12,1,7,5,12,1,4),
'11001101':(5,3,4,6,12,6,4,2,12,6,7),
'11011100':(5,3,2,8,3,8,2,6,3,8,12),
'11101100':(5,3,6,4,11,4,6,8,11,4,3),
'11001110':(5,3,8,2,7,2,8,4,7,2,11), 
'10110011':(5,3,8,2,9,2,8,6,9,2,1),
'00111011':(5,3,6,4,5,4,6,2,5,4,9),
'00110111':(5,3,2,8,10,8,2,4,10,8,5),
'01110011':(5,3,4,6,1,6,4,8,1,6,10),
'11000001':(6,3,2,9,4,2,10,9,7,12,8),
'11000010':(6,3,2,9,4,2,10,9,11,7,6),
'10010100':(6,3,12,1,9,3,1,12,10,6,5),
'10010010':(6,3,12,1,9,3,1,12,11,7,6),
'10101000':(6,3,4,5,8,1,5,4,2,3,11),
'10001010':(6,3,4,5,8,1,5,4,11,7,6),
'01101000':(6,3,10,3,11,1,3,10,5,8,9),
'01100001':(6,3,10,3,11,1,3,10,7,12,8),     
'01010100':(6,3,6,1,2,5,1,6,4,12,3),
'01000101':(6,3,6,1,2,5,1,6,7,12,8),
'00111000':(6,3,4,11,2,12,11,4,5,8,9),    
'00110100':(6,3,4,11,2,12,11,4,10,6,5),
'00101010':(6,3,7,3,2,6,7,2,9,4,1),
'10100010':(6,3,7,3,2,6,7,2,5,8,9),
'01010001':(6,3,3,8,7,4,8,3,1,2,10),
'00010101':(6,3,3,8,7,4,8,3,10,6,5),
'00011100':(6,3,8,10,6,9,10,8,4,12,3),
'00101100':(6,3,8,10,6,9,10,8,2,3,11),
'01001001':(6,3,7,9,5,12,9,7,1,2,10),
'00101001':(6,3,7,9,5,12,9,7,2,3,11),
'10000110':(6,3,11,5,10,7,5,11,9,4,1),
'00010110':(6,3,11,5,10,7,5,11,4,12,3),
'10000011':(6,3,12,6,11,8,6,12,9,4,1),
'01000011':(6,3,12,6,11,8,6,12,1,2,10),
'00111110':(6,3,2,4,9,2,9,10,8,12,7),
'00111101':(6,3,2,4,9,2,9,10,11,7,6),
'01101011':(6,3,12,9,1,3,12,1,5,6,10),
'01101101':(6,3,12,9,1,3,12,1,11,7,6),
'01010111':(6,3,4,8,5,1,4,5,11,3,2),
'01110101':(6,3,4,8,5,1,4,5,11,7,6),
'10010111':(6,3,10,11,3,1,10,3,9,8,5),
'10011110':(6,3,10,11,3,1,10,3,8,12,7),
'10101011':(6,3,6,2,1,5,6,1,3,12,4),
'10111010':(6,3,6,2,1,5,6,1,8,12,7),
'11000111':(6,3,4,2,11,12,4,11,9,8,5),
'11001011':(6,3,4,2,11,12,4,11,5,6,10),
'01011101':(6,3,7,2,3,6,2,7,1,4,9),
'00101010':(6,3,7,2,3,6,2,7,9,8,5),
'10101110':(6,3,3,7,8,4,3,8,10,2,1),
'11101010':(6,3,3,7,8,4,3,8,5,6,10),
'11100011':(6,3,8,6,10,9,8,10,3,12,4),    
'11010011':(6,3,8,6,10,9,8,10,11,3,2),
'10110110':(6,3,7,5,9,12,7,9,10,2,1),
'11010110':(6,3,7,5,9,12,7,9,11,3,2),
'01111001':(6,3,11,10,5,7,11,5,1,4,9),
'11101001':(6,3,11,10,5,7,11,5,3,12,4),
'01111100':(6,3,12,11,6,8,12,6,1,4,9),
'10111100':(6,3,12,11,6,8,12,6,10,2,1),	
'10100100':(7,3,9,4,1,2,3,11,10,6,5),
'10100001':(7,3,9,4,1,2,3,11,7,12,8),
'01011000':(7,3,1,2,10,4,12,3,5,8,9),
'01010010':(7,3,1,2,10,4,12,3,11,7,6),
'01001010':(7,3,1,2,10,5,8,9,11,7,6),
'00100101':(7,3,2,3,11,10,6,5,7,12,8),
'10000101':(7,3,9,4,1,10,6,5,7,12,8),
'00011010':(7,3,4,12,3,5,8,9,11,7,6),
'01011011':(7,3,1,4,9,11,3,2,5,6,10),
'01011110':(7,3,1,4,9,11,3,2,8,12,7),
'10100111':(7,3,10,2,1,3,12,4,9,8,5),
'10101101':(7,3,10,2,1,3,12,4,6,7,11),
'10110101':(7,3,10,2,1,9,8,5,6,7,11),
'11011010':(7,3,11,3,2,5,6,10,8,12,7),
'01111010':(7,3,1,4,9,5,6,10,8,12,7),
'11100101':(7,3,3,12,4,9,8,5,6,7,11),
'11110000':(8,2,9,11,10,11,9,12),
'01100110':(8,2,1,7,5,7,1,3),
'00001111':(8,2,11,9,10,9,11,12),
'10011001':(8,2,1,7,3,7,1,5),
'00110011':(8,2,8,2,4,2,8,6),
'11001100':(8,2,6,4,2,4,6,8),
'11100100':(9,4,3,11,6,3,6,5,3,5,4,4,5,9),
'01110010':(9,4,7,6,10,7,10,1,7,1,12,12,1,4),
'10110001':(9,4,1,9,8,1,8,7,1,7,2,2,7,11),
'11011000':(9,4,5,8,12,5,12,3,5,3,10,10,3,2),
'01001110':(9,4,8,9,1,8,1,2,8,2,7,7,2,11),	
'00100111':(9,4,12,8,5,12,5,10,12,10,3,3,10,2),
'10001101':(9,4,10,6,7,10,7,12,10,12,1,1,12,4),
'00011011':(9,4,6,11,3,6,3,4,6,4,5,5,4,9),
'11000011':(10,4,4,9,10,4,2,10,12,8,6,11,12,6),
'01101001':(10,4,1,11,10,1,3,11,9,5,7,7,12,9),
'00111100':(10,4,2,4,12,12,2,11,8,9,10,6,8,10),
'10010110':(10,4,9,12,3,9,3,1,11,7,5,10,11,5),
'01010101':(10,4,2,6,5,2,5,1,8,7,3,3,4,8),
'10101010':(10,4,1,5,8,1,8,4,7,6,2,3,7,2),
'11100010':(11,4,10,9,4,10,4,7,4,3,7,10,7,6),
'01110001':(11,4,11,10,1,1,8,11,1,4,8,11,8,7),
'10111000':(11,4,12,11,2,12,2,5,2,1,5,12,5,8),
'11010100':(11,4,9,12,3,9,3,6,3,2,6,9,6,5),
'01000111':(11,4,5,1,2,5,2,12,2,11,12,5,12,8),
'00110110':(11,4,7,5,10,7,10,4,4,10,2,7,4,12),
'01101100':(11,4,1,3,11,11,8,1,11,6,8,1,8,9),
'00011101':(11,4,9,10,6,6,3,9,6,7,3,9,3,4),
'00101011':(11,4,6,2,5,5,2,9,9,2,12,12,2,3), 			   
'10001110':(11,4,10,11,7,10,7,4,7,8,4,10,4,1),
'10010011':(11,4,3,1,9,3,9,6,9,8,6,3,6,11),
'11001001':(11,4,5,7,12,5,12,2,12,4,2,5,2,10),
'11100001':(12,4,4,11,9,11,10,9,4,3,11,7,12,8),
'01111000':(12,4,1,12,10,12,11,10,1,4,12,5,8,9),
'10110100':(12,4,2,9,11,9,12,11,2,1,9,10,6,5),
'11010010':(12,4,12,3,10,10,9,12,3,2,10,11,7,6),
'01010110':(12,4,1,2,7,7,5,1,2,11,7,4,12,3),
'10100110':(12,4,5,10,3,3,7,5,10,2,3,9,4,1),
'01101010':(12,4,7,6,1,1,3,7,6,10,1,5,8,9),
'01100101':(12,4,3,11,5,5,1,3,11,6,5,7,12,8),
'00101101':(12,4,10,6,12,12,9,10,6,7,12,2,3,11),
'01001011':(12,4,9,5,11,11,12,9,5,6,11,1,2,10),
'10000111':(12,4,12,8,10,10,11,12,8,5,10,9,4,1),
'00011110':(12,4,11,7,9,9,10,11,7,8,9,4,12,3),
'10011010':(12,4,5,8,3,3,1,5,8,12,3,11,7,6),
'10010101':(12,4,1,9,7,7,3,1,9,8,7,10,6,5),
'01011001':(12,4,3,4,5,5,7,3,4,9,5,1,2,10),
'10101001':(12,4,7,12,1,1,5,7,12,4,1,2,3,11),
'00111010':(12,4,4,12,6,6,2,4,12,7,6,5,8,9),
'10100011':(12,4,2,3,8,8,6,2,3,12,8,9,4,1),
'01010011':(12,4,6,11,4,4,8,6,11,3,4,1,2,10),
'00110101':(12,4,8,7,2,2,4,8,7,11,2,10,6,5),
'01011100':(12,4,8,9,2,2,6,8,9,1,2,4,12,3),
'11000101':(12,4,6,5,4,4,2,6,5,9,4,7,12,8),
'11001010':(12,4,2,10,8,8,4,2,10,5,8,11,7,6),
'10101100':(12,4,4,1,6,6,8,4,1,10,6,2,3,11),
'10100101':(13,4,9,4,1,2,3,11,10,6,5,7,12,8),
'01011010':(13,4,1,2,10,4,12,3,5,8,9,11,7,6),
'11101000':(14,4,3,11,10,3,10,8,3,8,4,10,5,8),
'01110100':(14,4,4,12,11,4,11,5,4,5,1,11,6,5),
'10110010':(14,4,1,9,12,1,12,6,1,6,2,12,7,6),
'11010001':(14,4,2,10,9,2,9,7,2,7,3,9,8,7),
'11000110':(14,4,9,4,2,9,2,7,9,7,5,2,11,7),
'00101110':(14,4,2,3,7,2,7,9,2,9,10,7,8,9),
'01100011':(14,4,10,1,3,10,3,8,10,8,6,3,12,8),
'01001101':(14,4,1,2,6,1,6,12,1,12,9,6,7,12),
'10001011':(14,4,6,11,12,6,12,1,6,1,5,12,4,1),
'00010111':(14,4,3,4,8,3,8,10,3,10,11,8,5,10),
'10011100':(14,4,12,3,1,12,1,6,12,6,8,1,10,6),
'00111001':(14,4,11,2,4,11,4,5,11,5,7,4,9,5),
}

##############################################################################
# segment dictionary
##############################################################################
SegmentDict = {
		'(1.0, 0.0, 0.0)'  											:	0,
		'(-1.0, 0.0, 0.0)' 											:	1,
		'(0.0, 1.0, 0.0)'  											:	2,
		'(0.0, -1.0, 0.0)' 											:	3,
		'(0.0, 0.0, 1.0)'  											:	4,
		'(0.0, 0.0, -1.0)' 											:	5,
		'(0.70711000000000002, 0.70711000000000002, 0.0)' 				:	6,
		'(0.70711000000000002, -0.70711000000000002, 0.0)' 				:	7,
		'(0.70711000000000002, 0.0, 0.70711000000000002)' 				:	8,
		'(0.70711000000000002, 0.0, -0.70711000000000002)' 				:	9,
		'(-0.70711000000000002, 0.70711000000000002, 0.0)' 				:	10,
		'(-0.70711000000000002, -0.70711000000000002, 0.0)' 				:	11,
		'(-0.70711000000000002, 0.0, 0.70711000000000002)'  				:	12,
		'(-0.70711000000000002, 0.0, -0.70711000000000002)'				: 	13,
        '(0.0, 0.70711000000000002, 0.70711000000000002)'  				: 	14,
        '(0.0, 0.70711000000000002, -0.70711000000000002)'  				:  	15,
        '(0.0, -0.70711000000000002, 0.70711000000000002)'  				:  	16,   
        '(0.0, -0.70711000000000002, -0.70711000000000002)' 				: 	17,
		'(0.57735000000000003, 0.57735000000000003, 0.57735000000000003)'  : 	18,
        '(0.57735000000000003, 0.57735000000000003, -0.57735000000000003)'  : 	19,	
        '(0.57735000000000003, -0.57735000000000003, 0.57735000000000003)'  : 	20,
        '(0.57735000000000003, -0.57735000000000003, -0.57735000000000003)' : 	21,
        '(-0.57735000000000003, 0.57735000000000003, 0.57735000000000003)'  : 	22,
        '(-0.57735000000000003, -0.57735000000000003, 0.57735000000000003)' : 	23,
        '(-0.57735000000000003, 0.57735000000000003, -0.57735000000000003)' : 	24,
        '(-0.57735000000000003, -0.57735000000000003, -0.57735000000000003)':	25,
		} 

##############################################################################
# vertice class
##############################################################################
class Vertice:
    def __init__(self,i,j,k,model,dims,scale,translate):# ,vertID
        self.I  = float(i)
        self.J  = float(j)
        self.K  = float(k)
        self.dims = dims
        self.scale = scale
        self.translate = translate
        self.m = model
        #self.id = vertID
        #vertID +=1 #true? 
        #self.string = "(" + str(self.I) + "," + str(self.J) + "," + str(self.K) + ")"
        self.string = "(%s , %s , %s)" % (self.I,self.J,self.K)
        self.MemberOf = []
        
        
        # vertdict.a
        # vertdict[n1pos] = vertID
        # TEST VERTICE CLASS!!! 
    
    def getVerticePosition(self):
       #def getvoxelpos(model,scale,dims,translate,i,j,k): #centroid!
       self.X = self.scale * ((self.I+.5)/self.dims) + self.translate[0]
       self.Y = self.scale * ((self.J+.5)/self.dims) + self.translate[1]  
       self.Z = self.scale * ((self.K+.5)/self.dims) + self.translate[2]   # klopt dit, centroid vs vertice? 
       return(self.X,self.Y,self.Z)
       
    def TagAsMember(self,surface):
        self.MemberOf.append(surface)
        
    def GetMembership(self):
        return self.MemberOf 
       
        
##############################################################################
# triangle class
##############################################################################       
class Triangle: 
    def __init__(self,n1,n2,n3,model,dims,scale,translate):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.model = model
        self.dims = dims
        self.scale = scale
        self.translate = translate
    def getNodeIndexes(self):
        return (self.n1,self.n2,self.n3)
        #self.id = triID
        #triID += 1 # werkt dit?  # niet nodig?
    def getNormalizedNormalVec(self):
        # create Vertice for each node
        Vert1 = Vertice(self.n1[0],self.n1[1],self.n1[2],self.model,self.dims,self.scale,self.translate)
        Vert2 = Vertice(self.n2[0],self.n2[1],self.n2[2],self.model,self.dims,self.scale,self.translate)
        Vert3 = Vertice(self.n3[0],self.n3[1],self.n3[2],self.model,self.dims,self.scale,self.translate)
        # get real pos for each Vertice, list as TriPos
        Vert1Pos = Vert1.getVerticePosition()
        Vert2Pos = Vert2.getVerticePosition()
        Vert3Pos = Vert3.getVerticePosition()
        TriPos = [Vert1Pos,Vert2Pos,Vert3Pos]
        # calc normalized normal vecor for Tri
        # get vectors Vert1Vert2 & Vert2Vert3
        TriVectors = np.subtract(TriPos[1:],TriPos[:-1])
        # get crossproduct of Vert1Vert2 & Vert2Vert3 (= surface normal)
        TriNorm = np.cross(TriVectors[0],TriVectors[1])+0.0
        # get length of surface normal
        length = np.linalg.norm(TriNorm)
        # divide each component of surface normal by length (= normalized surface normal)
        TriNormSurfNorm = np.around(TriNorm / length, decimals=5) # rounded, otherwise different values, equals not found
        # create string of tuple for segment dict        
        SegmVector = str(tuple(TriNormSurfNorm))
        return SegmVector
##############################################################################
# normal vec for 3 points
##############################################################################   

def getNormalizedNormalVec(tri_pos):
        # calc normalized normal vecor for Tri
        # get vectors Vert1Vert2 & Vert2Vert3
        tri_vectors = np.subtract(tri_pos[1:],tri_pos[:-1])
        # get crossproduct of Vert1Vert2 & Vert2Vert3 (= surface normal)segm_vector
        tri_norm = np.cross(tri_vectors[0],tri_vectors[1])+0.0
        # get length of surface normal
        length = np.linalg.norm(tri_norm)
        # divide each component of surface normal by length (= normalized surface normal)
        tri_norm_normalized = np.around(tri_norm / length, decimals=5) # rounded, otherwise different values, equals not found
        # create string of tuple for segment dict        
        segm_vector = str(tuple(tri_norm_normalized))
        return segm_vector
        
##############################################################################
# voxelblock class
##############################################################################

# class for Block of 8 voxels
class VoxelBlock:
    def __init__(self,i,j,k,model): # full model needed? or enter partial model only (block)
        self.I = i
        self.J = j
        self.K = k
        self.m = model
        
    def BlockIndex(self):
        blockIndex = "" 
        Block = self.m[self.I:self.I+2,self.J:self.J+2,self.K:self.K+2]
        order = [[0,0,0], [1,0,0], [1,0,1], [0,0,1], [0,1,0], [1,1,0], [1,1,1], [0,1,1]] # voxel numbering mirrored C-shape
        for index in order:
            blockIndex = blockIndex + str(int(Block[index[0],index[1],index[2]])) # cleaner way?
        #print blockIndex
        #print 10 * "*"
        #v1bool  = str(int(model[i  ,   j  ,    k  ]))
        #v2bool  = str(int(model[i+1,   j  ,    k  ]))
        #v3bool  = str(int(model[i+1,   j  ,    k+1]))
        #v4bool  = str(int(model[i  ,   j  ,    k+1]))
        #v5bool  = str(int(model[i  ,   j+1,    k  ]))
        #v6bool  = str(int(model[i+1,   j+1,    k  ]))
        #v7bool  = str(int(model[i+1,   j+1,    k+1]))
        #v8bool  = str(int(model[i  ,   j+1,    k+1]))
        #test order, is it correct? 
        return blockIndex
        
    def BlockEdges(self):
        e1 =  (1,[self.I+0.5, self.J    , self.K     ])  # turn into list or tuple? 
        e2 =  (2,[self.I+1.0, self.J    , self.K+0.5 ])
        e3 =  (3,[self.I+0.5, self.J    , self.K+1.0 ])
        e4 =  (4,[self.I    , self.J    , self.K+0.5 ])
        e5 =  (5,[self.I+0.5, self.J+1.0, self.K     ])
        e6 =  (6,[self.I+1.0, self.J+1.0, self.K+0.5 ])
        e7 =  (7,[self.I+0.5, self.J+1.0, self.K+1.0 ])
        e8 =  (8,[self.I    , self.J+1.0, self.K+0.5 ])
        e9 =  (9,[self.I    , self.J+0.5, self.K     ])
        e10 =(10,[self.I+1.0, self.J+0.5, self.K     ])
        e11 =(11,[self.I+1.0, self.J+0.5, self.K+1.0 ])
        e12 =(12,[self.I    , self.J+0.5, self.K+1.0 ])
        # better way? 
        return e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12        
##############################################################################
# write OBJ function
##############################################################################

def writeOBJ(vertlist,trilist,filename):
    print "number of triangles: " + str(len(trilist))
    print "number of vertices: " + str(len(vertlist))
    OBJ = open(filename, "w")
    OBJ.write('# Created with OBJ writer test version DM\n')
    OBJ.write('# COORDINATE_SYSTEM:  OGC_DEF PROJCS["Netherlands, Amersfoort RD 2008 datum, New System",GEOGCS["Amersfoort",DATUM["Amersfoort",SPHEROID["Bessel, 1841",6377397.155,299.1528153513275,AUTHORITY["EPSG","7004"]],AUTHORITY["EPSG","6289"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4289"]],PROJECTION["Stereographic"],PARAMETER["latitude_of_origin",52.1561605555556],PARAMETER["central_meridian",5.38763888888889],PARAMETER["scale_factor",0.9999079],PARAMETER["false_easting",155000],PARAMETER["false_northing",463000],UNIT["METER",1],AUTHORITY["EPSG","28992"]]\n')
    OBJ.write('# Number of Geometry Coordinates  : ' + str(len(vertlist)) + '\n')
    OBJ.write('# Number of Texture  Coordinates  : 0\n')
    OBJ.write('# Number of Normal   Coordinates  : 0\n')
    # loop through vertices and write to obj    
    for vert in vertlist:
        OBJ.write("v " + str(vert[0]) + " " + str(vert[1]) + " " + str(vert[2]) + "\n")
    OBJ.write('# Number of Elements in set       : ' + str(len(trilist)) + '\n') 
    # loop through triangles and write to obj
    for tri in trilist:
        OBJ.write("f " + str(tri[0]) + " " + str(tri[1]) + " " + str(tri[2]) + "\n")
    OBJ.write('# Total Number of Elements in file: ' + str(len(trilist)) + '\n') 
    OBJ.write('# EOF')
    OBJ.close()

##############################################################################
# write OBJ function segmented   STILL CHANGE THIS 
##############################################################################

def writeOBJ26segments(vertlist,SegmentTriList,filename):
    colorIndex = 1
    #print "number of triangles: " + str(len(trilist))
    print "number of vertices: " + str(len(vertlist))
    OBJ = open(filename, "w")
    OBJ.write('# RHINO\n\n')
    OBJ.write('mtllib 26Colors.mtl\n')
    # loop through vertices and write to obj    
    for vert in vertlist:
        OBJ.write("v " + str(vert[0]) + " " + str(vert[1]) + " " + str(vert[2]) + "\n")
    #OBJ.write('# Number of Elements in set       : ' + str(len(trilist)) + '\n') 
    # loop through triangles and write to obj
    for i in range(26):
        OBJ.write("usemtl Color%s\n" % (colorIndex) ) 
        colorIndex+=1
        for tri in SegmentTriList[i]:
            OBJ.write("f " + str(tri[0]) + " " + str(tri[1]) + " " + str(tri[2]) + "\n")
    OBJ.close()


##############################################################################
# writeOBJdetriangulated
##############################################################################
def writeOBJdetriangulated(vertlist,segmentlist,filename):
    colorIndex = 1
    print "number of vertices: " + str(len(vertlist))
    OBJ = open(filename, "w")
    OBJ.write('# RHINO\n\n')
    OBJ.write('mtllib 26Colors.mtl\n')
    # loop through vertices and write to obj    
    for vert in vertlist:
        OBJ.write("v " + str(vert[0]) + " " + str(vert[1]) + " " + str(vert[2]) + "\n")
    # loop through segments
    for segmentIND in range(0,len(segmentlist)):
        segment = segmentlist[segmentIND]
        OBJ.write("usemtl Color%s\n" % (colorIndex) ) 
        colorIndex+=1
        for surfaceIND in range(0,len(segment)):
            surface = segment[surfaceIND]
            surfacestring = "f " 
            for verticeIND in range(0,len(surface)-1):
                vertice = surface[verticeIND]
                surfacestring = surfacestring + (str(vertice) + " ")
            surfacestring = surfacestring + "\n"
            OBJ.write(surfacestring)
    OBJ.close()
##############################################################################
# normalize vdctor     not used everywhere(in tri) 
##############################################################################
def normalizevector(v):
    length = np.linalg.norm(v)
    norm = np.around(v/length,decimals=5)
    return norm  
    
##############################################################################
# angle between vectors 
##############################################################################
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)
    
def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle    
    
##############################################################################
# normalize vector     not used everywhere(in tri) 
##############################################################################    
def mergeline(p1,p2,p3):
    """compare the vector p1,p2 and p2,3
       if they are equivalent, retuen True
       if they are not equivalent, return False
    """
    v1 = np.subtract(p2,p1)
    v2 = np.subtract(p3,p2)
    if np.array_equiv(normalizevector(v2), normalizevector(v1)):
        #vectors equal
        return True
        
    else:
        #vectors not equal
        return False          


def flip_polygon(polygon):
    flipped_polygon = []
    for i in range(len(polygon)-1,-1,-1):
        print i
        flipped_polygon.append(polygon[i])
    return flipped_polygon


def main(array,dims,scale,translate):
    #print "start"
    #print array
    #print dims
    #print scale
    #print translate
    print "blablabla"
    trilist = []
    vertlist = []
    vertdict = {}
    dictIDtoIJK = {}
    vertID = 1
    SegmentTriList = [[] for i in range(26)]
    #SegmentEdgeDict = [{} for i in range(26)]
    #print len(SegmentTriList)
    # iterate over 3D-array 
    for k in range(0,dims-1):# -1 or -2? start at 0 or 1? denk fout
        for j in range(0,dims -1): 
            for i in range(0,dims -1):    
                Block = VoxelBlock(i,j,k,array)
                Edges = Block.BlockEdges()
                blockIndex = Block.BlockIndex()
                info = lookup[blockIndex]
                # get nodes for each triangle
                NumberOfTris = info[1]
                if NumberOfTris > 0:
                    count = 1
                    triple = [2,3,4]
                    # for every triangle get node ijk
                    while count <= NumberOfTris: 
                        # get ijk for n1 n2 and n3
                        trinodes = ((count-1)*3)+np.array(triple) # grow the triple for indexing 1st tri 2,3,4 / 2nd tri 5,6,7 etc.
                        n1 = info[trinodes[0]]
                        n1ijk = Edges[n1-1][1] #-1 because 1-12  list 0-11
                        n2 = info[trinodes[1]]
                        n2ijk = Edges[n2-1][1]
                        n3 = info[trinodes[2]]
                        n3ijk = Edges[n3-1][1]
                        Nijk = (n1ijk,n2ijk,n3ijk)
                        # WRITE IN A BETTER WAY ^^ 
                        IndexNodesTri = []
                        
                        # for every node (n1 n2 n3) check if it exists, and get vertID
                        for node in Nijk: 
                            # create vertice object
                            VERT = Vertice(node[0],node[1],node[2],array,dims,scale,translate)
                            # check in dictionary
                            #if not vertdict.has_key(VERT.string):  # same speed
                            #if VERT.string not in vertdict.keys():  # slow
                            if VERT.string not in vertdict:    
                                # if not present add to dict and list
                            
                                vertdict[VERT.string] = vertID
                                dictIDtoIJK[vertID] = (VERT.I,VERT.J,VERT.K)
                                # make reverse dict? from vertID to vertString
                                vertlist.append(VERT.getVerticePosition()) # klopt dit? zonder id is beter?  vertlist.append((vertID,VERT.getVerticePosition()))
                                vertID += 1
                            IndexNodesTri.append(vertdict[VERT.string])
                        # look up surf norm tup in dict, get back id 1-28, based on that assign to list inside list  "segmentlist" contains 28 lists
                        IndexNodesTri = tuple(IndexNodesTri)
                        # add triangle (tuple of 3 vertIDs) to trilist  
                        trilist.append(IndexNodesTri)
                        # make tri 
                        Tri = Triangle(n1ijk,n2ijk,n3ijk,array,dims,scale,translate)
                        # use SegmentDict pointer as index for SegmentList
                        SegmentTriList[SegmentDict[Tri.getNormalizedNormalVec()]].append(IndexNodesTri)
                        count += 1
                        
                        
                        # get real pos edges for each tri                         
                        
                        
    
    writeOBJ(vertlist,trilist,"fullmodel_MC.obj")
    writeOBJ26segments(vertlist,SegmentTriList,"fullmodel_MC26Segments.obj")
    
    
        
    
    # loop 28 for writeOBJ
    # write new writeOBJ function   28 with colours
    
    #try stuff for SegmentTrilist[0]
    #writeOBJ(vertlist,SegmentTriList[0],"testSegment0.obj")
    
    
    # LOOP THROUGH ALL SEGMENTS not only first
    
    
    
    
    
    SegmentEdgeList = [[] for i in range(26)]
    
    
    # APPEND ALL EDGES TO SegmentEdgeList 
    
    
    for SegmIND in range(26):
        Segment = SegmentTriList[SegmIND]
        for tri in Segment:
            edgeListsTemp = [list(tri[0:2]),list(tri[1:3]),[tri[2], tri[0]]]
            #print type(edgeListsTemp)
            #print edgeListsTemp
            #print "hier"+ 20 * "*"
            #print type(edgeTuples)
            #print edgeTuples 
            for edgeListTemp in edgeListsTemp:
                edgeListTemp = [min(edgeListTemp),max(edgeListTemp)] # maak hier list van!?
                SegmentEdgeList[SegmIND].append(edgeListTemp)
        # sort the list 
        SegmentEdgeList[SegmIND] = sorted(SegmentEdgeList[SegmIND])
    
        """OBJ = open("fullEdgeList", "w")
        for edge in edgeList:
            OBJ.write(str(edge) +'\n')    
        OBJ.close"""
    
    # loop from end to start! delete both double edges
    for SegmIND in range(26):
        Segment = SegmentEdgeList[SegmIND]
        i = len(Segment)-1
        while i > 0:
        #for i in range(len(edgeList)-1,-1,-1):
            if Segment[i] == Segment[i-1]:
                del Segment[i-1]
                del Segment[i-1]
                i -=2 #werkt dit echt? 
            else:
                i -=1
    #print SegmentEdgeList
    
    """OBJ = open("thinnedEdgeList", "w")
        for edge in edgeList:
        OBJ.write(str(edge) +'\n')    
        OBJ.close"""
    
    
    
    #OBJ = open("vertCheck", "w")
    #for vert in vertdict:
        #print vert
        #OBJ.write(str(vert) +'\n')    
    #OBJ.close
    
    dominoList = [[] for i in range(26)]
    # Set starting edge
    for segmentIND in range(0,26):
        dominoList[segmentIND] = [[SegmentEdgeList[segmentIND][0]]] # SHOULD BE LIST OF LISTS, FIX LATER  
        del SegmentEdgeList[segmentIND][0]
        segment = SegmentEdgeList[segmentIND]
        surfaceNumber = 0
        startEdge = SegmentEdgeList[segmentIND][0]
        #print "startedge = "+ str(startEdge)
                
        
        while len(SegmentEdgeList[segmentIND]) != 0:
            for edge in SegmentEdgeList[segmentIND]:
                edge = list(edge)
                #print dominoList[segmentIND][surfaceNumber][-1]
                if edge[1] == dominoList[segmentIND][surfaceNumber][-1][1]:
                    
                    SegmentEdgeList[segmentIND].remove(edge)
                    #print "FLIP"
                    edge = [edge[1],edge[0]]
                elif edge[0] == dominoList[segmentIND][surfaceNumber][-1][1]:
                    SegmentEdgeList[segmentIND].remove(edge)
                    
                if edge[0] == dominoList[segmentIND][surfaceNumber][-1][1]:
                    #"print first hit is"
                    dominoList[segmentIND][surfaceNumber].append(edge)
                    if edge[1] == startEdge[0]: 
                        #print "CLOSED!"
                        if len(SegmentEdgeList[segmentIND]) != 0:
                            surfaceNumber += 1
                            dominoList[segmentIND].append([])
                            startEdge = SegmentEdgeList[segmentIND][0]
                            dominoList[segmentIND][surfaceNumber].append(SegmentEdgeList[segmentIND].pop(0))
                i +=1
           
                    
    # depths = [[] for i in range(4)]
    #print dominoList

    dominoListThin = dominoList
    for segmentIND in range(0,len(dominoListThin)):
        segment = dominoListThin[segmentIND]
        for surfIND in range(0,len(segment)):
            surface = segment[surfIND]
            for edgeIND in range(0,len(surface)):
                edge = surface[edgeIND]
                #print edge
                # for each edge, take nly first vertice
                dominoListThin[segmentIND][surfIND][edgeIND] = edge[0]
            # for each surface, add first vertice to end
            dominoListThin[segmentIND][surfIND].append(dominoListThin[segmentIND][surfIND][0]) 
    #print dominoListThin    
    
    
    
    """
    # REAL POSITION
    dominoPosList = dominoListThin
    for segmentIND in range(0,len(dominoListThin)):
        segment = dominoListThin[segmentIND]
        for surfIND in range(0,len(segment)):
            surface = segment[surfIND]
            for vertIND in range(0,len(surface)):
                vert = surface[vertIND]
                vertIJK = dictIDtoIJK[vert]
                VERT = Vertice(vertIJK[0],vertIJK[1],vertIJK[2],model,dims,scale,translate)
                dominoPosList[segmentIND][surfIND][vertIND] = list(VERT.getVerticePosition())
    print dominoPosList
    """
    # run over iD's, get real pos for p1 p2 p3
    
    # THIN WITH MERGE LINE
    for segmentIND in range(0,len(dominoListThin)):
        segment = dominoListThin[segmentIND]   
        for surfIND in range(0,len(segment)):
            surface = segment[surfIND]
            for vertIND in range(len(surface)-2,0,-1):
                # get real positions
                p1 = surface[vertIND-1]
                p1IJK = dictIDtoIJK[p1]
                p1VERT = Vertice(p1IJK[0],p1IJK[1],p1IJK[2],array,dims,scale,translate)
                p1pos = p1VERT.getVerticePosition()
                
                p2 = surface[vertIND]
                p2IJK = dictIDtoIJK[p2]
                p2VERT = Vertice(p2IJK[0],p2IJK[1],p2IJK[2],array,dims,scale,translate)
                p2pos = p2VERT.getVerticePosition()
                
                p3 = surface[vertIND+1]
                p3IJK = dictIDtoIJK[p3]
                p3VERT = Vertice(p3IJK[0],p3IJK[1],p3IJK[2],array,dims,scale,translate)
                p3pos = p3VERT.getVerticePosition()
                
                #print p1,p2,p3
                if mergeline(p1pos,p2pos,p3pos) == True:
                    del surface[vertIND]
    
    #print dominoListThin[0]
    
    
    #print dominoListThin
    
    
    #testlist = [[1,1,1],[5,5,5],[10,10,10],[0,0,0]]
    #print np.mean(testlist,axis=0)
    
    #test_poly = [1,2,3,4,5]
    #print flip_polygon(test_poly)
    
    """
    print "****************************************"
    
    
    
    
    # CHECK ORIENTATIONS
    # for every segment, retrieve normal from dict
    for segment_index in range(0,26):
        
        print "****SEGMENT %s************" % segment_index
        # get segment normal vector
        print segment_index
        segment = dominoListThin[segment_index]
        print segment
        for key, val in SegmentDict.items():
            if val == segment_index:
                segment_normal = key
                break
        #print key    
        #print segment_normal
        segment_normal = segment_normal.translate(None, "()")
        #print 
        segment_normal_vec = [float(point) for point in segment_normal.split(",")]
        print segment_normal_vec
        
        
        
        # for each segment, get all polygons
        for poly_index in range(len(segment)):
            print "****POLYGON %s************" % poly_index
            poly = segment[poly_index]
            
            #CHECK ORIENTATION
            # calculate poly masspoint
            print poly
            poly_points = [vertlist[ind-1] for ind in poly]
            poly_mass_point = np.mean(poly_points,axis=0)
            m = np.mean(poly_points,axis=0)
            print poly_points
            print poly_mass_point
            
            
            P = np.add(poly_mass_point,segment_normal_vec)
            print segment_normal_vec
            print P
            
            #http://geomalgorithms.com/a01-_area.html
            for point_index in range(len(poly_points)-1):
                # create triangle to point P
                v_i,v_i1 = np.array(poly_points[point_index]), np.array(poly_points[point_index + 1])
                print "***********************"
                print "new tri"
                print np.subtract(v_i,P)
                print np.subtract(v_i1,P)
                area_vector = np.cross(np.subtract(v_i,P),np.subtract(v_i1,P))/2
                print area_vector
                
                
                dist_vi_vi1 = np.linalg.norm(v_i-v_i1)
                print "dist vi vi1 ="
                print dist_vi_vi1
                vec0 = np.subtract(v_i,v_i1)
                # FIRST POINT
                dist_m_vi = np.linalg.norm(m-v_i)
                #print "dist m vi ="
                #print dist_m_vi
                vec1 = np.subtract(v_i,m)
                a = angle_between(vec1,vec0)
                #print "angle alpha = "
                #print a
                dist_vi_B = abs(np.cos(a) * dist_m_vi)
                print "dist vi B ="
                print dist_vi_B
                
                # SECOND POINT 
                dist_m_vi1 = np.linalg.norm(m-v_i1)
                #print "dist m vi ="
                #print dist_m_vi
                vec2 = np.subtract(v_i1,m)
                b = angle_between(vec2,vec0)
                #print "angle beta = "
                #print b
                dist_vi1_B = abs(np.cos(b) * dist_m_vi1)
                print "dist vi1 B ="
                print dist_vi1_B
                
                if dist_vi_B < dist_vi_vi1 and dist_vi1_B < dist_vi_vi1:
                    print "point is on edge"
                    factor = dist_vi_B/dist_vi_vi1 
                    add_vec = factor * vec0
                    B = np.add(v_i,add_vec)
                    print v_i
                    print add_vec
                    print B
                    vec_3 = np.subtract(B,v_i,)
                    vec_4 = np.subtract(m,B)
                    a = angle_between(vec_3,vec_4)
                    print a
                    #vec_4 = np.subtract(v_i,B)
                    #vec_5 = np.subtract(B,v_i1)
                    #a = angle_between(vec_3,vec_4)
                    #print a
                elif dist_vi_B > dist_vi1_B:
                    print "point is in front of edge"
                
                elif dist_vi_B < dist_vi1_B:
                    print "point is behind edge"
                    # = np.add(v_i1,)
                else:
                    print "this is not possible?"
                #dist_m_vi = np.linalg.norm(m-v_i1)
                
                
                
                
                
                
                
                
                #print np.linalg.norm(poly_mass_point-v_i)
                dist_m_vi = np.linalg.norm(m-v_i)
                print "dist m vi ="
                print dist_m_vi
                #print "v_i"
                #print v_i
                #print "v_i1"
                #print v_i1
                #print "P"
                #print P
                vec1 = np.subtract(v_i,m)
                #print vec1
                vec2 = np.subtract(v_i,v_i1)
                #print vec2
                #print vec1
                #print vec2
                #print P
                a = angle_between(vec1,vec2)
                print "angle alpha = "
                print a
                #print np.cos(a)
                #print dist_m_vi
                dist_vi_vi1 = np.linalg.norm(v_i-v_i1)
                print "dist vi vi1 ="
                print dist_vi_vi1
                #print dist_vi_vi1
                #print np.cos(a) * dist_m_vi
                dist_vi_b = np.cos(a) * dist_m_vi
                print "dist vi b ="
                print dist_vi_b
                
                vec10 = np.subtract(v_i1,m)
                dist_m_vi = np.linalg.norm(m-v_i1)
                
                #print dist_vi_b
                #print dist_vi_vi1
                factor = dist_vi_b/dist_vi_vi1
                #print "FACTOR = "
                #print factor
                #factor = abs(factor)
                #print vec2
                #print factor * vec2
                B = np.add((factor * vec2),v_i)
                #print B
                vec_3 = np.subtract(v_i,B)
                vec_4 = np.subtract(B,m)
                a = angle_between(vec_3,vec_4)
                #print a
                vec_4 = np.subtract(v_i,B)
                vec_5 = np.subtract(B,v_i1)
                a = angle_between(vec_3,vec_4)
                #print a
                
            
            # check every polygon
            poly_points = []
            for point_index in poly:
                
                
                print point_index
                print vertlist[point_index-1]
            print poly
            print poly[0]-1
            print poly[1]-1
            print poly[2]-1
            print vertlist[poly[0]-1]
            print vertlist[poly[1]-1]
            print vertlist[poly[2]-1]
            # test real positions
            
            # test polygon orientation
        
            
                       
            for poly in segment: # turn into poly_index to change list item
            #print poly
            poly_test = [vertlist[poly[0]-1],vertlist[poly[1]-1],vertlist[poly[2]-1]] #only check first 3? 
            #print poly_test
            poly_normal = getNormalizedNormalVec(poly_test)
            print poly_normal
            if segment_normal == poly_normal:
                pass
                #print 'do nothing'
                
            else:
                pass
                #print 'flip poly'
                #print segment_normal
                #print poly_normal
            #np.array_equal(np.array(segment_normal) A,B)
            
         
        print segment
        #testtri = [ segment[0],segment[1],segment[2] ]
        v1 = vertlist[segment[0]-1]
        v2 = vertlist[segment[1]-1]
        v3 = vertlist[segment[2]-1]
        print getNormalizedNormalVec(v1,v2,v3)
        #Triangle(segment[0],segment[1],segment[2],tri)
        """
    
    
    
    
    
    #for segment in dominoListThin:
    #    testtri = [ segment[0],segment[1],segment[2] ]
    #    Triangle(segment[0],segment[1],segment[2],tri)
    # ADD HOLE CHECK HERE LATER 
    # TriPos = [Vert1Pos,Vert2Pos,Vert3Pos]
        # calc normalized normal vecor for Tri
    #TriVectors = np.subtract(TriPos[1:],TriPos[:-1])
    #TriNorm = np.cross(TriVectors[0],TriVectors[1])+0.0
    #length = np.linalg.norm(TriNorm)
    #TriNormSurfNorm = np.around(TriNorm / length, decimals=5) # rounded, otherwise different values, equals not found
    #SegmVector = str(tuple(TriNormSurfNorm))
    
    # RIGHT NOW, WRITE TO GML FOR EVERY OBJ     
    
    print 'BLABLABLA'  
    writeOBJdetriangulated(vertlist,dominoListThin,"fullmodel_MCDetriangulated26Segments.obj")
    #writeOBJdetriangulated(vertlist,dominoIDList,"testdetri.obj")     
    
    