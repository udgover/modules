# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2011 ArxSys
# 
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
# 
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Solal Jacob <sja@digital-forensic.org>

MSDocHeader = ({ "info" : { "os" : "None", "arch":"None", "name" : "Fib"},
	"descr" : {
			"Fib" : ((154),
			{
			   "FibBase" : (32, 0, "FibBase"),	#The fibBase
			   "csw"  : (2, 32), #count int16  in FibRgW must be 0x000E *2 (0xe * 2 == 28)
			   "fibRgW97" : (28, 34, "FibRgW97"), 
			   "cslw" : (2, 62), #count of 32 bit value in gibRgLw 0x16 * 4== 8
			   "fibRgLw97" : (88, 64, "FibRgLw97"),
			   "cbRgFcLcb" : (2, 152), #count of 64 bit value for fibRgFcLcbBlob table nfib -> cgbRgFcLcb
			   #"cswNew" count of 16 bit variable of fibRgCswNew depend of nfib et table ..
#			   "fibRgCswNew" if cswNew not 0 variable length ...
			}),
		        "FibBase" : ((32), # #Take care of bitfield and ms implem is false !
			{
			   "wIdent" : (2, 0), #Magic specifie this is a word file -> 0xA5EC
			   "nFib" : (2, 2), #0x00c1 00c0 00c2 version number of file, superseed by FibRgCswNew.nFibNew if present
			   "unused" : (2, 4), #product version
			   "lid" : (2, 6), #install language of the application 
			   "pnNext" : (2, 8), #offset of FIB who contains all the AutoText item,
			   "bitfield1" : (2, 10),
#			   "fDot" : (1, 9),  #specifies if it's a template
#			   "fGlsy" : (1, 10), #specifies if it contain only autotext 
#			   "fComplex" : (1, 11), #specifie if last save was incremental
#			   "fHasPic" : (1, 12), #specifie if there is pictuer !
#			   "cQuickSaves" : (4, 13), #if nFib < 0x09 specifie number of inc save done
#			   "fEncrypted" : (1, 14), #specifie if encrypted
#			   "fWichTblStm" : (1, 15), #specifie the table stream 0Table or 1Table
#			   "fReadOnlyRecommended" : (1, 16), #is the doc auto opened in RO mode
#			   "fWriteReservation" : (1, 17),  #is the doc have write recomendation pasword
#			   "fExtChar" : (1, 18), #? must be 1
#			   "fLoadOverride" : (1, 19), #overide font and lang
#			   "fFarEast" : (1, 20), #specifie the language was east asian
#			   "fObfuscated" : (1, 21), #the doc use XOR obfuscation
			   "nFibBack" : (2, 12),
			   "Ikey" : (4, 14), #if encrypted is 1 and fObfuscaiton 1 size of rc4 table or XOR password verifier
			   "envr" : (1, 18), #? must be 0
			   "bitfield2" : (1, 19),
			   "Chs" : (2 ,20),
			   "chsTables" : (2, 22),
			   "fcMin" : (4, 24),
			   "fcMac" : (4, 28),
#			   "fMac" : (1, 19), #must be 0
#			   "fEmptySpecial" : (1, 31) #msut be ..
#			   "fLoadOverridePage" : (1, 32), #overide ...
#			   "reserved1" : (1, 33),
#			   "reserved2" : (1, 34),
#			   "fSpare"0 : (3, 35), 
#			   "reserved3" : (2, 38),
#			   "reserved4" : (2, 40),
#			   "reserved5" : (4, 42),
#			   "reserved6" : (4, 46),
			}),
			"FibRgW97" : ((34),
			{
			  "Unused" : (24, 0), #nothing really interesting here, skipping ...
			}), 
			"FibRgLw97" : ((88),
			{
			  "cbMac" : (4, 0),			#64
			  "lProductCreated" : (4, 4), #"build date of the creator in special format #68
			  "lProductRevised" : (4, 8), #build date of file last modifier		#72
			  "ccpText" : (4, 12), #"length of the main doc text stream 1"		#76
			  "ccpFtn" : (4, 16), #length of footnote sub doc text stream		#80	
			  "ccpHdd" : (4, 20), #length of header sub doc				#84
			  "ccpMcr" : (4, 24), #length of macro ? should be 0 ?			#88
			  "ccpAtn" : (4, 28), #length of annoation				#92
			  "ccpEdn" : (4, 32), # "        endnote				#96
			  "ccpTxbx" : (4, 36), # "" 	text box subdoc				#100
			  "ccpHdrTxbx" : (4, 40), # "   header text box				#!04
			  "pnFbpChpFirst" : (4, 44), #						#108
			  "pnChpFirst" : (4, 48), # ..						#112
			  "cpnBteChp" : (4, 52), #						#116
			  "pnFbPapFirst" : (4, 56),						#120
			  "pnPapFirst" : (4, 60),						#124
			  "cpnBtePap" : (4, 64),						#128
			  "pbFbpLvcFirst" : (4, 68),						#132
			  "pnLvcFirst" : (4, 72),						#136
			  "cpnBteLvc" : (4, 76),						#140
			  "fcIslandFirst" : (4, 80),						#144
			  "fcIslandLim" : (4, 84)							#148
			}),
			"FibRgFcLcb97" : ((744),
			{
			"fcStshfOrig" : (4, 0),
			"lcbStshfOrig" : (4, 4),
			"fcStshf" : (4, 8),
			"lcbStshf" : (4, 12),
			"fcPlcffndRef" : (4, 16),
			"lcbPlcffndRef" : (4, 20),
			"fcPlcffndTxt" : (4, 24),
			"lcbPlcffndTxt" : (4, 28),
			"fcPlcfandRef" : (4, 32),
			"lcbPlcfandRef" : (4, 36),
			"fcPlcfandTxt" : (4, 40),
			"lcbPlcfandTxt" : (4, 44),
			"fcPlcfSed" : (4, 48),
			"lcbPlcfSed" : (4, 52),
			"fcPlcPad" : (4, 56),
			"lcbPlcPad" : (4, 60),
			"fcPlcfPhe" : (4, 64),
			"lcbPlcfPhe" : (4, 68),
			"fcSttbfGlsy" : (4, 72),
			"lcbSttbfGlsy" : (4, 76),
			"fcPlcfGlsy" : (4, 80),
			"lcbPlcfGlsy" : (4, 84),
			"fcPlcfHdd" : (4, 88),
			"lcbPlcfHdd" : (4, 92),
			"fcPlcfBteChpx" : (4, 96),
			"lcbPlcfBteChpx" : (4, 100),
			"fcPlcfBtePapx" : (4, 104),
			"lcbPlcfBtePapx" : (4, 108),
			"fcPlcfSea" : (4, 112),
			"lcbPlcfSea" : (4, 116),
			"fcSttbfFfn" : (4, 120),
			"lcbSttbfFfn" : (4, 124),
			"fcPlcfFldMom" : (4, 128),
			"lcbPlcfFldMom" : (4, 132),
			"fcPlcfFldHdr" : (4, 136),
			"lcbPlcfFldHdr" : (4, 140),
			"fcPlcfFldFtn" : (4, 144),
			"lcbPlcfFldFtn" : (4, 148),
			"fcPlcfFldAtn" : (4, 152),
			"lcbPlcfFldAtn" : (4, 156),
			"fcPlcfFldMcr" : (4, 160),
			"lcbPlcfFldMcr" : (4, 164),
			"fcSttbfBkmk" : (4, 168),
			"lcbSttbfBkmk" : (4, 172),
			"fcPlcfBkf" : (4, 176),
			"lcbPlcfBkf" : (4, 180),
			"fcPlcfBkl" : (4, 184),
			"lcbPlcfBkl" : (4, 188),
			"fcCmds" : (4, 192),
			"lcbCmds" : (4, 196),
			"fcUnused1" : (4, 200),
			"lcbUnused1" : (4, 204),
			"fcSttbfMcr" : (4, 208),
			"lcbSttbfMcr" : (4, 212),
			"fcPrDrvr" : (4, 216),
			"lcbPrDrvr" : (4, 220),
			"fcPrEnvPort" : (4, 224),
			"lcbPrEnvPort" : (4, 228),
			"fcPrEnvLand" : (4, 232),
			"lcbPrEnvLand" : (4, 236),
			"fcWss" : (4, 240),
			"lcbWss" : (4, 244),
			"fcDop" : (4, 248),
			"lcbDop" : (4, 252),
			"fcSttbfAssoc" : (4, 256),
			"lcbSttbfAssoc" : (4, 260),
			"fcClx" : (4, 264),
			"lcbClx" : (4, 268),
			"fcPlcfPgdFtn" : (4, 272),
			"lcbPlcfPgdFtn" : (4, 276),
			"fcAutosaveSource" : (4, 280),
			"lcbAutosaveSource" : (4, 284),
			"fcGrpXstAtnOwners" : (4, 288),
			"lcbGrpXstAtnOwners" : (4, 292),
			"fcSttbfAtnBkmk" : (4, 296),
			"lcbSttbfAtnBkmk" : (4, 300),
			"fcUnused2" : (4, 304),
			"lcbUnused2" : (4, 308),
			"fcUnused3" : (4, 312),
			"lcbUnused3" : (4, 316),
			"fcPlcSpaMom" : (4, 320),
			"lcbPlcSpaMom" : (4, 324),
			"fcPlcSpaHdr" : (4, 328),
			"lcbPlcSpaHdr" : (4, 332),
			"fcPlcfAtnBkf" : (4, 336),
			"lcbPlcfAtnBkf" : (4, 340),
			"fcPlcfAtnBkl" : (4, 344),
			"lcbPlcfAtnBkl" : (4, 348),
			"fcPms" : (4, 352),
			"lcbPms" : (4, 356),
			"fcFormFldSttbs" : (4, 360),
			"lcbFormFldSttbs" : (4, 364),
			"fcPlcfendRef" : (4, 368),
			"lcbPlcfendRef" : (4, 372),
			"fcPlcfendTxt" : (4, 376),
			"lcbPlcfendTxt" : (4, 380),
			"fcPlcfFldEdn" : (4, 384),
			"lcbPlcfFldEdn" : (4, 388),
			"fcUnused4" : (4, 392),
			"lcbUnused4" : (4, 396),
			"fcDggInfo" : (4, 400),
			"lcbDggInfo" : (4, 404),
			"fcSttbfRMark" : (4, 408),
			"lcbSttbfRMark" : (4, 412),
			"fcSttbfCaption" : (4, 416),
			"lcbSttbfCaption" : (4, 420),
			"fcSttbfAutoCaption" : (4, 424),
			"lcbSttbfAutoCaption" : (4, 428),
			"fcPlcfWkb" : (4, 432),
			"lcbPlcfWkb" : (4, 436),
			"fcPlcfSpl" : (4, 440),
			"lcbPlcfSpl" : (4, 444),
			"fcPlcftxbxTxt" : (4, 448),
			"lcbPlcftxbxTxt" : (4, 452),
			"fcPlcfFldTxbx" : (4, 456),
			"lcbPlcfFldTxbx" : (4, 460),
			"fcPlcfHdrtxbxTxt" : (4, 464),
			"lcbPlcfHdrtxbxTxt" : (4, 468),
			"fcPlcffldHdrTxbx" : (4, 472),
			"lcbPlcffldHdrTxbx" : (4, 476),
			"fcStwUser" : (4, 480),
			"lcbStwUser" : (4, 484),
			"fcSttbTtmbd" : (4, 488),
			"lcbSttbTtmbd" : (4, 492),
			"fcCookieData" : (4, 496),
			"lcbCookieData" : (4, 500),
			"fcPgdMotherOldOld" : (4, 504),
			"lcbPgdMotherOldOld" : (4, 508),
			"fcBkdMotherOldOld" : (4, 512),
			"lcbBkdMotherOldOld" : (4, 516),
			"fcPgdFtnOldOld" : (4, 520),
			"lcbPgdFtnOldOld" : (4, 524),
			"fcBkdFtnOldOld" : (4, 528),
			"lcbBkdFtnOldOld" : (4, 532),
			"fcPgdEdnOldOld" : (4, 536),
			"lcbPgdEdnOldOld" : (4, 540),
			"fcBkdEdnOldOld" : (4, 544),
			"lcbBkdEdnOldOld" : (4, 548),
			"fcSttbfIntlFld" : (4, 552),
			"lcbSttbfIntlFld" : (4, 556),
			"fcRouteSlip" : (4, 560),
			"lcbRouteSlip" : (4, 564),
			"fcSttbSavedBy" : (4, 568),
			"lcbSttbSavedBy" : (4, 572),
			"fcSttbFnm" : (4, 576),
			"lcbSttbFnm" : (4, 580),
			"fcPlfLst" : (4, 584),
			"lcbPlfLst" : (4, 588),
			"fcPlfLfo" : (4, 592),
			"lcbPlfLfo" : (4, 596),
			"fcPlcfTxbxBkd" : (4, 600),
			"lcbPlcfTxbxBkd" : (4, 604),
			"fcPlcfTxbxHdrBkd" : (4, 608),
			"lcbPlcfTxbxHdrBkd" : (4, 612),
			"fcDocUndoWord9" : (4, 616),
			"lcbDocUndoWord9" : (4, 620),
			"fcRgbUse" : (4, 624),
			"lcbRgbUse" : (4, 628),
			"fcUsp" : (4, 632),
			"lcbUsp" : (4, 636),
			"fcUskf" : (4, 640),
			"lcbUskf" : (4, 644),
			"fcPlcupcRgbUse" : (4, 648),
			"lcbPlcupcRgbUse" : (4, 652),
			"fcPlcupcUsp" : (4, 656),
			"lcbPlcupcUsp" : (4, 660),
			"fcSttbGlsyStyle" : (4, 664),
			"lcbSttbGlsyStyle" : (4, 668),
			"fcPlgosl" : (4, 672),
			"lcbPlgosl" : (4, 676),
			"fcPlcocx" : (4, 680),
			"lcbPlcocx" : (4, 684),
			"fcPlcfBteLvc" : (4, 688),
			"lcbPlcfBteLvc" : (4, 692),
			"dwLowDateTime" : (4, 696),
			"dwHighDateTime" : (4, 700),
			"fcPlcfLvcPre10" : (4, 704),
			"lcbPlcfLvcPre10" : (4, 708),
			"fcPlcfAsumy" : (4, 712),
			"lcbPlcfAsumy" : (4, 716),
			"fcPlcfGram" : (4, 720),
			"lcbPlcfGram" : (4, 724),
			"fcSttbListNames" : (4, 728),
			"lcbSttbListNames" : (4, 732),
			"fcSttbfUssr" : (4, 736),
			"lcbSttbfUssr" : (4, 740),	
			}),
			"FibRgFcLcb2000" : ((864),  #self 120
			{
			"FibRgFcLcb97" : (744, 0, "FibRgFcLcb97"),
			"fcPlcfTch" : (4, 744),
			"lcbPlcfTch" : (4, 748),
			"fcRmdThreading" : (4, 752),
			"lcbRmdThreading" : (4, 756),
			"fcMid" : (4, 760),
			"lcbMid" : (4, 764),
			"fcSttbRgtplc" : (4, 768),
			"lcbSttbRgtplc" : (4, 772),
			"fcMsoEnvelope" : (4, 776),
			"lcbMsoEnvelope" : (4, 780),
			"fcPlcfLad" : (4, 784),
			"lcbPlcfLad" : (4, 788),
			"fcRgDofr" : (4, 792),
			"lcbRgDofr" : (4, 796),
			"fcPlcosl" : (4, 800),
			"lcbPlcosl" : (4, 804),
			"fcPlcfCookieOld" : (4, 808),
			"lcbPlcfCookieOld" : (4, 812),
			"fcPgdMotherOld" : (4, 816),
			"lcbPgdMotherOld" : (4, 820),
			"fcBkdMotherOld" : (4, 824),
			"lcbBkdMotherOld" : (4, 828),
			"fcPgdFtnOld" : (4, 832),
			"lcbPgdFtnOld" : (4, 836),
			"fcBkdFtnOld" : (4, 840),
			"lcbBkdFtnOld" : (4, 844),
			"fcPgdEdnOld" : (4, 848),
			"lcbPgdEdnOld" : (4, 852),
			"fcBkdEdnOld" : (4, 856),
			"lcbBkdEdnOld" : (4, 860),
			}),
			"FibRgFcLcb2002" : ((1088), #self 224
			{
			"FibRgFcLcb2000" : (864, 0, "FibRgFcLcb2000"),
			"fcUnused1" : (4, 864),
			"lcbUnused1" : (4, 868),
			"fcPlcfPgp" : (4, 872),
			"lcbPlcfPgp" : (4, 876),
			"fcPlcfuim" : (4, 880),
			"lcbPlcfuim" : (4, 884),
			"fcPlfguidUim" : (4, 888),
			"lcbPlfguidUim" : (4, 892),
			"fcAtrdExtra" : (4, 896),
			"lcbAtrdExtra" : (4, 900),
			"fcPlrsid" : (4, 904),
			"lcbPlrsid" : (4, 908),
			"fcSttbfBkmkFactoid" : (4, 912),
			"lcbSttbfBkmkFactoid" : (4, 916),
			"fcPlcfBkfFactoid" : (4, 920),
			"lcbPlcfBkfFactoid" : (4, 924),
			"fcPlcfcookie" : (4, 928),
			"lcbPlcfcookie" : (4, 932),
			"fcPlcfBklFactoid" : (4, 936),
			"lcbPlcfBklFactoid" : (4, 940),
			"fcFactoidData" : (4, 944),
			"lcbFactoidData" : (4, 948),
			"fcDocUndo" : (4, 952),
			"lcbDocUndo" : (4, 956),
			"fcSttbfBkmkFcc" : (4, 960),
			"lcbSttbfBkmkFcc" : (4, 964),
			"fcPlcfBkfFcc" : (4, 968),
			"lcbPlcfBkfFcc" : (4, 972),
			"fcPlcfBklFcc" : (4, 976),
			"lcbPlcfBklFcc" : (4, 980),
			"fcSttbfbkmkBPRepairs" : (4, 984),
			"lcbSttbfbkmkBPRepairs" : (4, 988),
			"fcPlcfbkfBPRepairs" : (4, 992),
			"lcbPlcfbkfBPRepairs" : (4, 996),
			"fcPlcfbklBPRepairs" : (4, 1000),
			"lcbPlcfbklBPRepairs" : (4, 1004),
			"fcPmsNew" : (4, 1008),
			"lcbPmsNew" : (4, 1012),
			"fcODSO" : (4, 1016),
			"lcbODSO" : (4, 1020),
			"fcPlcfpmiOldXP" : (4, 1024),
			"lcbPlcfpmiOldXP" : (4, 1028),
			"fcPlcfpmiNewXP" : (4, 1032),
			"lcbPlcfpmiNewXP" : (4, 1036),
			"fcPlcfpmiMixedXP" : (4, 1040),
			"lcbPlcfpmiMixedXP" : (4, 1044),
			"fcUnused2" : (4, 1048),
			"lcbUnused2" : (4, 1052),
			"fcPlcffactoid" : (4, 1056),
			"lcbPlcffactoid" : (4, 1060),
			"fcPlcflvcOldXP" : (4, 1064),
			"lcbPlcflvcOldXP" : (4, 1068),
			"fcPlcflvcNewXP" : (4, 1072),
			"lcbPlcflvcNewXP" : (4, 1076),
			"fcPlcflvcMixedXP" : (4, 1080),
			"lcbPlcflvcMixedXP" : (4, 1084),
			}),
			"FibRgFcLcb2003" : ((1312), #self 224
			{
			"FibRgFcLcb2002" : (1088, 0, "FibRgFcLcb2002"),
			"fcHplxsdr" : (4, 1088),
			"lcbHplxsdr" : (4, 1092),
			"fcSttbfBkmkSdt" : (4, 1096),
			"lcbSttbfBkmkSdt" : (4, 1100),
			"fcPlcfBkfSdt" : (4, 1104),
			"lcbPlcfBkfSdt" : (4, 1108),
			"fcPlcfBklSdt" : (4, 1112),
			"lcbPlcfBklSdt" : (4, 1116),
			"fcCustomXForm" : (4, 1120),
			"lcbCustomXForm" : (4, 1124),
			"fcSttbfBkmkProt" : (4, 1128),
			"lcbSttbfBkmkProt" : (4, 1132),
			"fcPlcfBkfProt" : (4, 1136),
			"lcbPlcfBkfProt" : (4, 1140),
			"fcPlcfBklProt" : (4, 1144),
			"lcbPlcfBklProt" : (4, 1148),
			"fcSttbProtUser" : (4, 1152),
			"lcbSttbProtUser" : (4, 1156),
			"fcUnused" : (4, 1160),
			"lcbUnused" : (4, 1164),
			"fcPlcfpmiOld" : (4, 1168),
			"lcbPlcfpmiOld" : (4, 1172),
			"fcPlcfpmiOldInline" : (4, 1176),
			"lcbPlcfpmiOldInline" : (4, 1180),
			"fcPlcfpmiNew" : (4, 1184),
			"lcbPlcfpmiNew" : (4, 1188),
			"fcPlcfpmiNewInline" : (4, 1192),
			"lcbPlcfpmiNewInline" : (4, 1196),
			"fcPlcflvcOld" : (4, 1200),
			"lcbPlcflvcOld" : (4, 1204),
			"fcPlcflvcOldInline" : (4, 1208),
			"lcbPlcflvcOldInline" : (4, 1212),
			"fcPlcflvcNew" : (4, 1216),
			"lcbPlcflvcNew" : (4, 1220),
			"fcPlcflvcNewInline" : (4, 1224),
			"lcbPlcflvcNewInline" : (4, 1228),
			"fcPgdMother" : (4, 1232),
			"lcbPgdMother" : (4, 1236),
			"fcBkdMother" : (4, 1240),
			"lcbBkdMother" : (4, 1244),
			"fcAfdMother" : (4, 1248),
			"lcbAfdMother" : (4, 1252),
			"fcPgdFtn" : (4, 1256),
			"lcbPgdFtn" : (4, 1260),
			"fcBkdFtn" : (4, 1264),
			"lcbBkdFtn" : (4, 1268),
			"fcAfdFtn" : (4, 1272),
			"lcbAfdFtn" : (4, 1276),
			"fcPgdEdn" : (4, 1280),
			"lcbPgdEdn" : (4, 1284),
			"fcBkdEdn" : (4, 1288),
			"lcbBkdEdn" : (4, 1292),
			"fcAfdEdn" : (4, 1296),
			"lcbAfdEdn" : (4, 1300),
			"fcAfd" : (4, 1304),
			"lcbAfd" : (4, 1308),
			}),
			"FibRgFcLcb2007" : ((1464), #self 152 
			{
			"FibRgFcLcb2003" : (1312, 0, "FibRgFcLcb2003"),
			"fcPlcfmthd" : (4, 1312),
			"lcbPlcfmthd" : (4, 1316),
			"fcSttbfBkmkMoveFrom" : (4, 1320),
			"lcbSttbfBkmkMoveFrom" : (4, 1324),
			"fcPlcfBkfMoveFrom" : (4, 1328),
			"lcbPlcfBkfMoveFrom" : (4, 1332),
			"fcPlcfBklMoveFrom" : (4, 1336),
			"lcbPlcfBklMoveFrom" : (4, 1340),
			"fcSttbfBkmkMoveTo" : (4, 1344),
			"lcbSttbfBkmkMoveTo" : (4, 1348),
			"fcPlcfBkfMoveTo" : (4, 1352),
			"lcbPlcfBkfMoveTo" : (4, 1356),
			"fcPlcfBklMoveTo" : (4, 1360),
			"lcbPlcfBklMoveTo" : (4, 1364),
			"fcUnused1" : (4, 1368),
			"lcbUnused1" : (4, 1372),
			"fcUnused2" : (4, 1376),
			"lcbUnused2" : (4, 1380),
			"fcUnused3" : (4, 1384),
			"lcbUnused3" : (4, 1388),
			"fcSttbfBkmkArto" : (4, 1392),
			"lcbSttbfBkmkArto" : (4, 1396),
			"fcPlcfBkfArto" : (4, 1400),
			"lcbPlcfBkfArto" : (4, 1404),
			"fcPlcfBklArto" : (4, 1408),
			"lcbPlcfBklArto" : (4, 1412),
			"fcArtoData" : (4, 1416),
			"lcbArtoData" : (4, 1420),
			"fcUnused4" : (4, 1424),
			"lcbUnused4" : (4, 1428),
			"fcUnused5" : (4, 1432),
			"lcbUnused5" : (4, 1436),
			"fcUnused6" : (4, 1440),
			"lcbUnused6" : (4, 1444),
			"fcOssTheme" : (4, 1448),
			"lcbOssTheme" : (4, 1452),
			"fcColorSchemeMapping" : (4, 1456),
			"lcbColorSchemeMapping" : (4, 1460),
			}),
		  	"FibRgCswNewData2000" : ((4),
			{
			  "nFibNew" : (2, 0),
			  "nQuickSavesNew" : (2,2),
			}),
			"FibRgCswNewData2007" : ((10),
			{
			  "nFibNew" : (2, 0),
			  "nQuickSaveNew" : (2, 2),
			  "lidThemeOther" : (2, 4),
			  "lidThemeFE" : (2, 6),
			  "lidThemeCS" : (2, 8),
			})
		    }
		})

