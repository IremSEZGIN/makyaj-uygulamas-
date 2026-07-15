import json
import re

text = """AÇIK TEN + SICAK ALT TON
--------------------------------------------------

gunluk:
allık: AL-10, AL-13, AL-14
ruj: RJ-09, RJ-15, RJ-20, RJ-34, RJ-44
far: FR-02, FR-04, FR-05, FR-06
eyeliner: EL-10, EL-11
kontür: KN-01, KN-02, KN-06
aydınlatıcı: AY-03, AY-04, AY-05
bronzer: BR-01, BR-02, BR-03

is:
allık: AL-07, AL-11, AL-13
ruj: RJ-09, RJ-20, RJ-21, RJ-31
far: FR-02, FR-06, FR-07, FR-08
eyeliner: EL-09, EL-10
kontür: KN-01, KN-02, KN-06
aydınlatıcı: AY-03, AY-05
bronzer: BR-01, BR-02

aksam:
allık: AL-03, AL-10, AL-19
ruj: RJ-16, RJ-18, RJ-25, RJ-30, RJ-49
far: FR-08, FR-10, FR-42, FR-43, FR-47
eyeliner: EL-01, EL-09, EL-13
kontür: KN-06, KN-07, KN-08
aydınlatıcı: AY-07, AY-08, AY-09
bronzer: BR-03, BR-04, BR-07

dugun:
allık: AL-10, AL-13, AL-14
ruj: RJ-15, RJ-20, RJ-32, RJ-34, RJ-44
far: FR-03, FR-05, FR-06, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-14
kontür: KN-02, KN-06, KN-07
aydınlatıcı: AY-03, AY-05, AY-09
bronzer: BR-01, BR-02, BR-03

parti:
allık: AL-04, AL-18, AL-21
ruj: RJ-17, RJ-24, RJ-30, RJ-36, RJ-49
far: FR-43, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-28
kontür: KN-07, KN-08, KN-09
aydınlatıcı: AY-07, AY-08, AY-10
bronzer: BR-04, BR-05, BR-07

plaj:
allık: AL-01, AL-10, AL-12, AL-14, AL-21
ruj: RJ-02, RJ-15, RJ-34, RJ-36, RJ-44, RJ-48
far: FR-05, FR-06, FR-08, FR-41, FR-46
eyeliner: EL-10, EL-11, EL-14
kontür: KN-06, KN-07
aydınlatıcı: AY-07, AY-08, AY-19
bronzer: BR-02, BR-03, BR-07

--------------------------------------------------
AÇIK TEN + SOĞUK ALT TON
--------------------------------------------------

gunluk:
allık: AL-02, AL-08, AL-09, AL-16
ruj: RJ-02, RJ-03, RJ-31, RJ-33, RJ-45
far: FR-02, FR-03, FR-13, FR-18
eyeliner: EL-07, EL-08, EL-14
kontür: KN-01, KN-02, KN-03
aydınlatıcı: AY-01, AY-12, AY-13, AY-15
bronzer: BR-01, BR-08, BR-13

is:
allık: AL-08, AL-13, AL-15
ruj: RJ-03, RJ-27, RJ-31, RJ-33, RJ-40
far: FR-02, FR-03, FR-18, FR-38
eyeliner: EL-04, EL-06, EL-14
kontür: KN-01, KN-02, KN-04
aydınlatıcı: AY-01, AY-12, AY-13
bronzer: BR-01, BR-08, BR-13

aksam:
allık: AL-06, AL-08, AL-15, AL-17
ruj: RJ-04, RJ-08, RJ-12, RJ-27, RJ-46
far: FR-18, FR-20, FR-21, FR-22, FR-23
eyeliner: EL-01, EL-04, EL-18
kontür: KN-03, KN-04, KN-13
aydınlatıcı: AY-12, AY-13, AY-16
bronzer: BR-08, BR-13

dugun:
allık: AL-02, AL-08, AL-09, AL-13, AL-16
ruj: RJ-03, RJ-05, RJ-31, RJ-33, RJ-38, RJ-45, RJ-46
far: FR-03, FR-13, FR-15, FR-18, FR-19, FR-20
eyeliner: EL-04, EL-09, EL-14
kontür: KN-01, KN-02, KN-13
aydınlatıcı: AY-01, AY-12, AY-13, AY-15
bronzer: BR-01, BR-08

parti:
allık: AL-04, AL-05, AL-17, AL-20
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-29, RJ-37, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31
eyeliner: EL-01, EL-02, EL-18, EL-19, EL-20
kontür: KN-04, KN-05, KN-13
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13

plaj:
allık: AL-01, AL-02, AL-04, AL-05, AL-16, AL-20
ruj: RJ-02, RJ-05, RJ-38, RJ-44, RJ-50
far: FR-03, FR-05, FR-13, FR-19, FR-46
eyeliner: EL-14, EL-17, EL-23, EL-24
kontür: KN-01, KN-02, KN-13
aydınlatıcı: AY-12, AY-13, AY-15
bronzer: BR-01, BR-08, BR-13

--------------------------------------------------
AÇIK TEN + NÖTR ALT TON
--------------------------------------------------

gunluk:
allık: AL-02, AL-10, AL-13, AL-14, AL-16
ruj: RJ-02, RJ-03, RJ-09, RJ-15, RJ-20, RJ-31, RJ-33, RJ-44
far: FR-02, FR-03, FR-04, FR-05, FR-06, FR-13
eyeliner: EL-09, EL-10, EL-14
kontür: KN-01, KN-02, KN-03
aydınlatıcı: AY-01, AY-03, AY-05, AY-12
bronzer: BR-01, BR-02, BR-08

is:
allık: AL-07, AL-08, AL-13, AL-15
ruj: RJ-09, RJ-20, RJ-21, RJ-27, RJ-31, RJ-33, RJ-40
far: FR-02, FR-06, FR-07, FR-08, FR-18
eyeliner: EL-04, EL-09, EL-10, EL-14
kontür: KN-01, KN-02, KN-04
aydınlatıcı: AY-01, AY-03, AY-05, AY-12
bronzer: BR-01, BR-02, BR-08

aksam:
allık: AL-03, AL-06, AL-08, AL-15, AL-19
ruj: RJ-04, RJ-12, RJ-16, RJ-18, RJ-23, RJ-25, RJ-27, RJ-46
far: FR-08, FR-10, FR-18, FR-20, FR-42, FR-47
eyeliner: EL-01, EL-04, EL-09, EL-13
kontür: KN-03, KN-04, KN-07
aydınlatıcı: AY-03, AY-09, AY-12, AY-13
bronzer: BR-02, BR-03, BR-08

dugun:
allık: AL-02, AL-08, AL-10, AL-13, AL-14, AL-16
ruj: RJ-03, RJ-15, RJ-20, RJ-31, RJ-32, RJ-33, RJ-38, RJ-44, RJ-45
far: FR-03, FR-05, FR-06, FR-13, FR-18, FR-46
eyeliner: EL-09, EL-10, EL-14
kontür: KN-01, KN-02, KN-06
aydınlatıcı: AY-01, AY-03, AY-09, AY-12
bronzer: BR-01, BR-02, BR-08

parti:
allık: AL-04, AL-05, AL-06, AL-17, AL-20
ruj: RJ-01, RJ-06, RJ-08, RJ-17, RJ-24, RJ-29, RJ-30, RJ-37, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-31, FR-43, FR-46, FR-47
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-20
kontür: KN-04, KN-05, KN-08
aydınlatıcı: AY-07, AY-12, AY-13, AY-16
bronzer: BR-03, BR-08, BR-13

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-20
ruj: RJ-02, RJ-05, RJ-15, RJ-34, RJ-36, RJ-44, RJ-48, RJ-50
far: FR-05, FR-06, FR-08, FR-41, FR-46
eyeliner: EL-10, EL-11, EL-14, EL-17, EL-23
kontür: KN-02, KN-06, KN-07
aydınlatıcı: AY-07, AY-08, AY-12, AY-19
bronzer: BR-02, BR-03, BR-07, BR-08

--------------------------------------------------
BUĞDAY TEN + SICAK ALT TON
--------------------------------------------------

gunluk:
allık: AL-10, AL-11, AL-12, AL-14, AL-19
ruj: RJ-10, RJ-13, RJ-15, RJ-20, RJ-21, RJ-34, RJ-44
far: FR-04, FR-05, FR-06, FR-08, FR-09
eyeliner: EL-09, EL-10, EL-11
kontür: KN-06, KN-07, KN-08
aydınlatıcı: AY-05, AY-07, AY-08, AY-09
bronzer: BR-02, BR-03, BR-04, BR-07

is:
allık: AL-07, AL-11, AL-19
ruj: RJ-10, RJ-13, RJ-21, RJ-22, RJ-23, RJ-42
far: FR-06, FR-07, FR-08, FR-09, FR-10, FR-11
eyeliner: EL-09, EL-10, EL-11
kontür: KN-07, KN-08, KN-09
aydınlatıcı: AY-05, AY-07, AY-09
bronzer: BR-03, BR-04, BR-07

aksam:
allık: AL-03, AL-11, AL-18, AL-19, AL-21
ruj: RJ-16, RJ-18, RJ-19, RJ-25, RJ-30, RJ-36, RJ-48, RJ-49
far: FR-08, FR-10, FR-11, FR-42, FR-43, FR-44, FR-47
eyeliner: EL-01, EL-02, EL-09, EL-13
kontür: KN-08, KN-09, KN-10, KN-14
aydınlatıcı: AY-07, AY-08, AY-09, AY-10
bronzer: BR-04, BR-05, BR-07, BR-10

dugun:
allık: AL-07, AL-10, AL-12, AL-14
ruj: RJ-15, RJ-20, RJ-25, RJ-32, RJ-34, RJ-35, RJ-44, RJ-48
far: FR-05, FR-06, FR-08, FR-10, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-14
kontür: KN-07, KN-08, KN-09
aydınlatıcı: AY-07, AY-08, AY-09
bronzer: BR-03, BR-04, BR-07

parti:
allık: AL-04, AL-18, AL-21
ruj: RJ-17, RJ-24, RJ-30, RJ-36, RJ-41, RJ-49
far: FR-43, FR-44, FR-45, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-13, EL-28
kontür: KN-09, KN-10, KN-11, KN-14
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-05, BR-06, BR-07, BR-10

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-21
ruj: RJ-02, RJ-15, RJ-34, RJ-36, RJ-44, RJ-48
far: FR-05, FR-06, FR-08, FR-10, FR-41, FR-42, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-14, EL-17, EL-23
kontür: KN-07, KN-08
aydınlatıcı: AY-07, AY-08, AY-10, AY-19
bronzer: BR-03, BR-04, BR-07, BR-10

--------------------------------------------------
BUĞDAY TEN + SOĞUK ALT TON
--------------------------------------------------

gunluk:
allık: AL-02, AL-08, AL-15, AL-16
ruj: RJ-03, RJ-04, RJ-31, RJ-33, RJ-40, RJ-45
far: FR-03, FR-13, FR-18, FR-19
eyeliner: EL-07, EL-08, EL-09, EL-14
kontür: KN-04, KN-05, KN-13, KN-15
aydınlatıcı: AY-03, AY-12, AY-13, AY-14
bronzer: BR-08, BR-09, BR-13

is:
allık: AL-07, AL-08, AL-15, AL-19
ruj: RJ-21, RJ-22, RJ-23, RJ-27, RJ-31, RJ-40, RJ-42
far: FR-06, FR-08, FR-10, FR-18, FR-38
eyeliner: EL-04, EL-06, EL-09, EL-14
kontür: KN-04, KN-05, KN-13, KN-15
aydınlatıcı: AY-03, AY-12, AY-13
bronzer: BR-08, BR-09, BR-13

aksam:
allık: AL-06, AL-08, AL-15, AL-17, AL-20
ruj: RJ-04, RJ-08, RJ-12, RJ-14, RJ-27, RJ-28, RJ-46, RJ-47, RJ-50
far: FR-18, FR-20, FR-21, FR-22, FR-23, FR-24
eyeliner: EL-01, EL-02, EL-04, EL-18
kontür: KN-05, KN-13, KN-15, KN-16
aydınlatıcı: AY-12, AY-13, AY-14, AY-16
bronzer: BR-08, BR-13, BR-14

dugun:
allık: AL-02, AL-08, AL-09, AL-13, AL-15, AL-16
ruj: RJ-03, RJ-05, RJ-31, RJ-33, RJ-38, RJ-39, RJ-40, RJ-45, RJ-46
far: FR-03, FR-13, FR-18, FR-19, FR-20, FR-46
eyeliner: EL-04, EL-09, EL-10, EL-14
kontür: KN-04, KN-05, KN-13
aydınlatıcı: AY-03, AY-12, AY-13, AY-15
bronzer: BR-08, BR-09, BR-13

parti:
allık: AL-04, AL-05, AL-06, AL-17, AL-20
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-12, RJ-29, RJ-37, RJ-43, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31, FR-32
eyeliner: EL-01, EL-02, EL-18, EL-19, EL-20, EL-25
kontür: KN-13, KN-15, KN-16, KN-17
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14

plaj:
allık: AL-01, AL-04, AL-05, AL-16, AL-20
ruj: RJ-02, RJ-05, RJ-34, RJ-38, RJ-44, RJ-50
far: FR-05, FR-13, FR-19, FR-41, FR-46
eyeliner: EL-10, EL-14, EL-17, EL-23, EL-24
kontür: KN-04, KN-13
aydınlatıcı: AY-12, AY-13, AY-15, AY-19
bronzer: BR-08, BR-09, BR-13

--------------------------------------------------
BUĞDAY TEN + NÖTR ALT TON
--------------------------------------------------

gunluk:
allık: AL-02, AL-08, AL-10, AL-13, AL-14, AL-16, AL-19
ruj: RJ-03, RJ-09, RJ-15, RJ-20, RJ-21, RJ-31, RJ-33, RJ-44
far: FR-02, FR-04, FR-05, FR-06, FR-08, FR-18
eyeliner: EL-09, EL-10, EL-11, EL-14
kontür: KN-04, KN-06, KN-07
aydınlatıcı: AY-03, AY-05, AY-07, AY-12
bronzer: BR-02, BR-03, BR-08

is:
allık: AL-07, AL-08, AL-11, AL-13, AL-15, AL-19
ruj: RJ-09, RJ-10, RJ-13, RJ-20, RJ-21, RJ-22, RJ-23, RJ-27, RJ-31, RJ-40, RJ-42
far: FR-02, FR-06, FR-07, FR-08, FR-09, FR-10, FR-18, FR-38
eyeliner: EL-04, EL-06, EL-09, EL-10, EL-14
kontür: KN-04, KN-06, KN-07, KN-13
aydınlatıcı: AY-03, AY-05, AY-09, AY-12
bronzer: BR-02, BR-03, BR-08, BR-09

aksam:
allık: AL-03, AL-06, AL-08, AL-15, AL-19, AL-21
ruj: RJ-04, RJ-12, RJ-16, RJ-18, RJ-23, RJ-25, RJ-27, RJ-30, RJ-46, RJ-48
far: FR-08, FR-10, FR-11, FR-18, FR-20, FR-42, FR-43, FR-47
eyeliner: EL-01, EL-02, EL-04, EL-09, EL-13
kontür: KN-07, KN-08, KN-09, KN-13
aydınlatıcı: AY-07, AY-09, AY-12, AY-13
bronzer: BR-03, BR-04, BR-08, BR-10

dugun:
allık: AL-02, AL-07, AL-08, AL-10, AL-13, AL-14, AL-15, AL-16
ruj: RJ-03, RJ-15, RJ-20, RJ-31, RJ-32, RJ-33, RJ-34, RJ-38, RJ-39, RJ-44, RJ-45
far: FR-03, FR-05, FR-06, FR-13, FR-18, FR-19, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-13, EL-14
kontür: KN-04, KN-06, KN-07
aydınlatıcı: AY-03, AY-07, AY-09, AY-12
bronzer: BR-02, BR-03, BR-08

parti:
allık: AL-04, AL-05, AL-06, AL-17, AL-18, AL-20, AL-21
ruj: RJ-01, RJ-06, RJ-08, RJ-17, RJ-24, RJ-29, RJ-30, RJ-37, RJ-43, RJ-47, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-31, FR-43, FR-45, FR-46, FR-47
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-19, EL-20
kontür: KN-08, KN-09, KN-13, KN-16
aydınlatıcı: AY-07, AY-10, AY-12, AY-16
bronzer: BR-04, BR-07, BR-08, BR-13

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-20, AL-21
ruj: RJ-02, RJ-05, RJ-15, RJ-34, RJ-36, RJ-38, RJ-44, RJ-48, RJ-50
far: FR-05, FR-06, FR-08, FR-10, FR-41, FR-42, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-14, EL-17, EL-23, EL-24
kontür: KN-06, KN-07, KN-08
aydınlatıcı: AY-07, AY-08, AY-12, AY-19
bronzer: BR-03, BR-04, BR-07, BR-08

--------------------------------------------------
ESMER TEN + SICAK ALT TON
--------------------------------------------------

gunluk:
allık: AL-03, AL-11, AL-12, AL-19
ruj: RJ-13, RJ-16, RJ-18, RJ-21, RJ-22, RJ-25, RJ-42
far: FR-06, FR-08, FR-10, FR-11, FR-42
eyeliner: EL-09, EL-10, EL-11
kontür: KN-09, KN-10, KN-11, KN-14
aydınlatıcı: AY-07, AY-08, AY-09, AY-10
bronzer: BR-04, BR-07, BR-10, BR-11

is:
allık: AL-03, AL-11, AL-19
ruj: RJ-21, RJ-22, RJ-23, RJ-25, RJ-42
far: FR-08, FR-10, FR-11, FR-12
eyeliner: EL-09, EL-10, EL-11
kontür: KN-09, KN-10, KN-14
aydınlatıcı: AY-07, AY-09, AY-10
bronzer: BR-07, BR-10, BR-11

aksam:
allık: AL-03, AL-18, AL-19, AL-21
ruj: RJ-17, RJ-24, RJ-30, RJ-36, RJ-41, RJ-48, RJ-49
far: FR-10, FR-11, FR-42, FR-43, FR-44, FR-45, FR-47
eyeliner: EL-01, EL-02, EL-09, EL-13
kontür: KN-10, KN-11, KN-14, KN-16
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-10, BR-11, BR-12, BR-15

dugun:
allık: AL-10, AL-11, AL-12, AL-14, AL-19
ruj: RJ-18, RJ-25, RJ-30, RJ-34, RJ-35, RJ-42, RJ-44, RJ-48
far: FR-05, FR-08, FR-10, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-13
kontür: KN-09, KN-10, KN-14
aydınlatıcı: AY-07, AY-08, AY-09, AY-10
bronzer: BR-07, BR-10, BR-11

parti:
allık: AL-18, AL-21
ruj: RJ-17, RJ-24, RJ-30, RJ-36, RJ-41, RJ-49
far: FR-43, FR-44, FR-45, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-13, EL-25, EL-28
kontür: KN-10, KN-11, KN-16, KN-17
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-10, BR-11, BR-12, BR-15

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-21
ruj: RJ-15, RJ-34, RJ-36, RJ-44, RJ-48
far: FR-05, FR-08, FR-10, FR-41, FR-42, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-17, EL-23, EL-24
kontür: KN-08, KN-09, KN-10
aydınlatıcı: AY-07, AY-08, AY-10, AY-19
bronzer: BR-07, BR-10, BR-11, BR-12

--------------------------------------------------
ESMER TEN + SOĞUK ALT TON
--------------------------------------------------

gunluk:
allık: AL-06, AL-08, AL-15, AL-17, AL-20
ruj: RJ-04, RJ-12, RJ-27, RJ-28, RJ-40, RJ-46
far: FR-18, FR-20, FR-21, FR-23
eyeliner: EL-09, EL-13, EL-14, EL-18
kontür: KN-13, KN-15, KN-16
aydınlatıcı: AY-12, AY-13, AY-14, AY-16
bronzer: BR-08, BR-13, BR-14

is:
allık: AL-08, AL-15, AL-19
ruj: RJ-22, RJ-23, RJ-27, RJ-28, RJ-40, RJ-42
far: FR-08, FR-10, FR-18, FR-38
eyeliner: EL-04, EL-09, EL-13, EL-14
kontür: KN-13, KN-15, KN-16
aydınlatıcı: AY-12, AY-13, AY-14
bronzer: BR-08, BR-13, BR-14

aksam:
allık: AL-06, AL-15, AL-17, AL-20
ruj: RJ-06, RJ-07, RJ-08, RJ-12, RJ-14, RJ-24, RJ-29, RJ-43, RJ-50
far: FR-20, FR-21, FR-22, FR-23, FR-24, FR-25, FR-31
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-20
kontür: KN-15, KN-16, KN-17
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14, BR-16

dugun:
allık: AL-08, AL-09, AL-15, AL-16, AL-20
ruj: RJ-05, RJ-31, RJ-33, RJ-38, RJ-39, RJ-40, RJ-45, RJ-46
far: FR-03, FR-18, FR-19, FR-20, FR-23, FR-46
eyeliner: EL-09, EL-13, EL-14
kontür: KN-13, KN-15, KN-16
aydınlatıcı: AY-12, AY-13, AY-15, AY-16
bronzer: BR-08, BR-13, BR-14

parti:
allık: AL-05, AL-06, AL-17, AL-20
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-12, RJ-29, RJ-37, RJ-43, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31, FR-32
eyeliner: EL-01, EL-02, EL-18, EL-19, EL-20, EL-25
kontür: KN-15, KN-16, KN-17
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14, BR-16

plaj:
allık: AL-01, AL-04, AL-05, AL-16, AL-20
ruj: RJ-05, RJ-34, RJ-38, RJ-44, RJ-50
far: FR-05, FR-13, FR-19, FR-41, FR-46
eyeliner: EL-14, EL-17, EL-23, EL-24
kontür: KN-13, KN-15
aydınlatıcı: AY-12, AY-13, AY-15, AY-19
bronzer: BR-08, BR-13, BR-14

--------------------------------------------------
ESMER TEN + NÖTR ALT TON
--------------------------------------------------

gunluk:
allık: AL-03, AL-08, AL-11, AL-15, AL-19
ruj: RJ-13, RJ-16, RJ-21, RJ-22, RJ-23, RJ-27, RJ-40, RJ-42
far: FR-06, FR-08, FR-10, FR-11, FR-18, FR-42
eyeliner: EL-09, EL-10, EL-13, EL-14
kontür: KN-09, KN-13, KN-14, KN-15
aydınlatıcı: AY-07, AY-09, AY-12, AY-13
bronzer: BR-07, BR-08, BR-10, BR-13

is:
allık: AL-07, AL-08, AL-11, AL-15, AL-19
ruj: RJ-21, RJ-22, RJ-23, RJ-27, RJ-40, RJ-42
far: FR-08, FR-10, FR-11, FR-18, FR-38
eyeliner: EL-04, EL-09, EL-10, EL-13
kontür: KN-09, KN-13, KN-14, KN-15
aydınlatıcı: AY-07, AY-09, AY-12
bronzer: BR-07, BR-08, BR-10, BR-13

aksam:
allık: AL-03, AL-06, AL-15, AL-17, AL-19, AL-21
ruj: RJ-06, RJ-12, RJ-14, RJ-16, RJ-18, RJ-24, RJ-27, RJ-30, RJ-41, RJ-46, RJ-48
far: FR-10, FR-11, FR-20, FR-21, FR-42, FR-43, FR-47
eyeliner: EL-01, EL-02, EL-09, EL-13, EL-18
kontür: KN-10, KN-13, KN-15, KN-16
aydınlatıcı: AY-07, AY-10, AY-12, AY-13
bronzer: BR-08, BR-10, BR-13, BR-14

dugun:
allık: AL-08, AL-10, AL-13, AL-14, AL-15, AL-16, AL-19
ruj: RJ-15, RJ-20, RJ-31, RJ-32, RJ-34, RJ-38, RJ-39, RJ-40, RJ-44, RJ-45
far: FR-03, FR-05, FR-06, FR-18, FR-19, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-13, EL-14
kontür: KN-09, KN-13, KN-14
aydınlatıcı: AY-07, AY-09, AY-12, AY-13
bronzer: BR-07, BR-08, BR-10

parti:
allık: AL-04, AL-05, AL-06, AL-17, AL-18, AL-20, AL-21
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-17, RJ-24, RJ-29, RJ-30, RJ-37, RJ-43, RJ-47, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-31, FR-43, FR-45, FR-46, FR-47
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-19, EL-20
kontür: KN-13, KN-15, KN-16, KN-17
aydınlatıcı: AY-07, AY-10, AY-12, AY-16
bronzer: BR-08, BR-10, BR-13, BR-14

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-20, AL-21
ruj: RJ-15, RJ-34, RJ-36, RJ-38, RJ-44, RJ-48, RJ-50
far: FR-05, FR-06, FR-08, FR-10, FR-41, FR-42, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-14, EL-17, EL-23, EL-24
kontür: KN-09, KN-13, KN-14
aydınlatıcı: AY-07, AY-08, AY-12, AY-19
bronzer: BR-07, BR-08, BR-10, BR-13

--------------------------------------------------
KOYU TEN + SICAK ALT TON
--------------------------------------------------

gunluk:
allık: AL-03, AL-18, AL-19, AL-21
ruj: RJ-17, RJ-24, RJ-30, RJ-36, RJ-41, RJ-42, RJ-49
far: FR-10, FR-11, FR-42, FR-43, FR-44, FR-47
eyeliner: EL-09, EL-11, EL-13
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-10, BR-11, BR-12, BR-15, BR-16

is:
allık: AL-03, AL-11, AL-19
ruj: RJ-21, RJ-22, RJ-23, RJ-25, RJ-42, RJ-49
far: FR-08, FR-10, FR-11, FR-12, FR-42
eyeliner: EL-09, EL-10, EL-11, EL-13
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-10, AY-11
bronzer: BR-10, BR-11, BR-14, BR-16

aksam:
allık: AL-18, AL-19, AL-21
ruj: RJ-17, RJ-24, RJ-29, RJ-30, RJ-36, RJ-41, RJ-49
far: FR-43, FR-44, FR-45, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-13, EL-25, EL-28
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-11, BR-12, BR-15, BR-16

dugun:
allık: AL-10, AL-12, AL-14, AL-19, AL-21
ruj: RJ-25, RJ-30, RJ-34, RJ-36, RJ-42, RJ-44, RJ-48, RJ-49
far: FR-05, FR-08, FR-10, FR-46, FR-47, FR-48
eyeliner: EL-09, EL-10, EL-13
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-10, BR-11, BR-12

parti:
allık: AL-18, AL-21
ruj: RJ-17, RJ-24, RJ-29, RJ-30, RJ-36, RJ-41, RJ-49
far: FR-43, FR-45, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-13, EL-25, EL-28
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-08, AY-10, AY-11
bronzer: BR-11, BR-12, BR-15, BR-16

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-21
ruj: RJ-34, RJ-36, RJ-44, RJ-48
far: FR-05, FR-08, FR-10, FR-41, FR-42, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-17, EL-23, EL-24
kontür: KN-16, KN-17
aydınlatıcı: AY-07, AY-08, AY-10, AY-19
bronzer: BR-10, BR-11, BR-12, BR-15

--------------------------------------------------
KOYU TEN + SOĞUK ALT TON
--------------------------------------------------

gunluk:
allık: AL-06, AL-17, AL-20
ruj: RJ-06, RJ-08, RJ-12, RJ-29, RJ-37, RJ-43, RJ-50
far: FR-20, FR-21, FR-22, FR-23, FR-24
eyeliner: EL-09, EL-13, EL-18, EL-20
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14, BR-16

is:
allık: AL-08, AL-15, AL-17, AL-19
ruj: RJ-23, RJ-27, RJ-28, RJ-40, RJ-41, RJ-43
far: FR-10, FR-18, FR-20, FR-38
eyeliner: EL-04, EL-09, EL-13, EL-14
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-12, AY-13, AY-16
bronzer: BR-08, BR-13, BR-14, BR-16

aksam:
allık: AL-06, AL-17, AL-20
ruj: RJ-06, RJ-07, RJ-08, RJ-12, RJ-24, RJ-29, RJ-37, RJ-43, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31, FR-32
eyeliner: EL-01, EL-02, EL-18, EL-19, EL-20, EL-25
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14, BR-16

dugun:
allık: AL-08, AL-09, AL-15, AL-16, AL-20
ruj: RJ-05, RJ-31, RJ-33, RJ-37, RJ-38, RJ-39, RJ-45, RJ-46, RJ-50
far: FR-13, FR-19, FR-20, FR-23, FR-46
eyeliner: EL-09, EL-13, EL-14, EL-18
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-12, AY-13, AY-15, AY-16
bronzer: BR-08, BR-13, BR-14

parti:
allık: AL-05, AL-06, AL-17, AL-20
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-29, RJ-37, RJ-43, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-31, FR-32
eyeliner: EL-01, EL-02, EL-18, EL-19, EL-20, EL-25
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-12, AY-15, AY-16, AY-17
bronzer: BR-08, BR-13, BR-14, BR-16

plaj:
allık: AL-01, AL-04, AL-05, AL-16, AL-20
ruj: RJ-05, RJ-34, RJ-38, RJ-44, RJ-50
far: FR-05, FR-13, FR-19, FR-41, FR-46
eyeliner: EL-14, EL-17, EL-23, EL-24
kontür: KN-16, KN-17
aydınlatıcı: AY-12, AY-13, AY-15, AY-19
bronzer: BR-08, BR-13, BR-14

--------------------------------------------------
KOYU TEN + NÖTR ALT TON
--------------------------------------------------

gunluk:
allık: AL-03, AL-06, AL-17, AL-19, AL-20, AL-21
ruj: RJ-12, RJ-17, RJ-24, RJ-27, RJ-29, RJ-30, RJ-41, RJ-43, RJ-49
far: FR-10, FR-11, FR-20, FR-42, FR-43, FR-47
eyeliner: EL-09, EL-13, EL-18
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-10, AY-12, AY-16
bronzer: BR-08, BR-10, BR-13, BR-16

is:
allık: AL-08, AL-11, AL-15, AL-19
ruj: RJ-21, RJ-22, RJ-23, RJ-27, RJ-40, RJ-41, RJ-42
far: FR-08, FR-10, FR-11, FR-18, FR-38
eyeliner: EL-04, EL-09, EL-10, EL-13
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-10, AY-12
bronzer: BR-08, BR-10, BR-13, BR-14

aksam:
allık: AL-06, AL-17, AL-18, AL-19, AL-20, AL-21
ruj: RJ-06, RJ-08, RJ-17, RJ-24, RJ-29, RJ-30, RJ-41, RJ-43, RJ-49, RJ-50
far: FR-21, FR-23, FR-43, FR-45, FR-46, FR-47, FR-48
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-20
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-10, AY-12, AY-16
bronzer: BR-08, BR-10, BR-13, BR-16

dugun:
allık: AL-08, AL-10, AL-13, AL-14, AL-15, AL-16, AL-20
ruj: RJ-15, RJ-31, RJ-33, RJ-34, RJ-38, RJ-39, RJ-44, RJ-45, RJ-46, RJ-50
far: FR-03, FR-05, FR-13, FR-19, FR-46, FR-47
eyeliner: EL-09, EL-10, EL-13, EL-14
kontür: KN-16, KN-17
aydınlatıcı: AY-07, AY-12, AY-13, AY-15
bronzer: BR-08, BR-10, BR-13

parti:
allık: AL-04, AL-05, AL-06, AL-17, AL-18, AL-20, AL-21
ruj: RJ-01, RJ-06, RJ-07, RJ-08, RJ-17, RJ-24, RJ-29, RJ-30, RJ-37, RJ-43, RJ-47, RJ-50
far: FR-21, FR-22, FR-23, FR-24, FR-31, FR-43, FR-45, FR-46, FR-47
eyeliner: EL-01, EL-02, EL-13, EL-18, EL-19, EL-20, EL-25
kontür: KN-16, KN-17, KN-18
aydınlatıcı: AY-07, AY-10, AY-12, AY-16
bronzer: BR-08, BR-10, BR-13, BR-16

plaj:
allık: AL-01, AL-04, AL-10, AL-12, AL-14, AL-20, AL-21
ruj: RJ-05, RJ-34, RJ-36, RJ-38, RJ-44, RJ-48, RJ-50
far: FR-05, FR-06, FR-08, FR-10, FR-13, FR-41, FR-46, FR-47
eyeliner: EL-10, EL-11, EL-14, EL-17, EL-23, EL-24
kontür: KN-16, KN-17
aydınlatıcı: AY-07, AY-08, AY-12, AY-19
bronzer: BR-08, BR-10, BR-13, BR-16
"""

blocks = re.split(r'--------------------------------------------------\n([A-ZÇĞIİÖŞÜ ]+ TEN \+ [A-ZÇĞIİÖŞÜ ]+ ALT TON)\n--------------------------------------------------', text)

dart_code = "Map<String, Map<String, Map<String, List<String>>>> makeupMatrix = {\n"

for i in range(1, len(blocks), 2):
    group_name = blocks[i].strip()
    content = blocks[i+1]
    
    parts = group_name.split(' + ')
    skin = parts[0].replace(' TEN', '').strip()
    undertone = parts[1].replace(' ALT TON', '').strip()
    
    dart_code += f"  '{skin}_{undertone}': {{\n"
    
    events = re.split(r'\n(gunluk|is|aksam|dugun|parti|plaj):\n', content)
    for j in range(1, len(events), 2):
        event_id = events[j]
        event_content = events[j+1]
        
        dart_code += f"    '{event_id}': {{\n"
        lines = event_content.strip().split('\n')
        for line in lines:
            if ':' in line:
                k, v = line.split(':', 1)
                items = [f"'{x.strip()}'" for x in v.split(',')]
                dart_code += f"      '{k.strip()}': [{', '.join(items)}],\n"
        dart_code += "    },\n"
    dart_code += "  },\n"

dart_code += "};\n"

with open('matrix.dart', 'w', encoding='utf-8') as f:
    f.write(dart_code)

print("matrix.dart created")
