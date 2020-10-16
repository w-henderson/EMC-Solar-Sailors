from modules import coordinateSystems

def test_Vector():
    testVector = coordinateSystems.Vector(3, 4)

    assert testVector.magnitude == 5
    assert testVector.normalized == coordinateSystems.Vector(0.6, 0.8)
    assert testVector.normalized.magnitude == 1

    assert testVector.toTuple() == (3, 4)
    assert testVector.toPoint() == (-7, -6, 13, 14)
    assert testVector.toPerpendicular() == coordinateSystems.Vector(4, -3)
    assert testVector.toHeliocentric() == coordinateSystems.Heliocentric(60.74752762, 4.387518661)

def test_Heliocentric():
    testHeliocentric = coordinateSystems.Heliocentric(30, 1)

    assert testHeliocentric.toVector() == coordinateSystems.Vector(1085, 756.5063509461097)

def test_Sun():
    assert coordinateSystems.Sun.position == coordinateSystems.Vector(960, 540)