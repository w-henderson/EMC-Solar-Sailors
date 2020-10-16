from modules import spacecraft, coordinateSystems

def test_addForce():
    sail = spacecraft.SolarSail(1000, 1000, 0, coordinateSystems.Vector(0, 0))
    assert sail.force == coordinateSystems.Vector(0, 0)

    sail.addForce(coordinateSystems.Vector(100, 100))
    assert sail.force == coordinateSystems.Vector(1.6711229946524065e-07, 1.6711229946524065e-07)
    sail.addForce(coordinateSystems.Vector(100, 100))
    assert sail.force == coordinateSystems.Vector(1.6711229946524065e-07 * 2, 1.6711229946524065e-07 * 2)

def test_updatePosition():
    sail = spacecraft.SolarSail(1000, 1000, 0, coordinateSystems.Vector(0, 0))
    assert sail.velocity == coordinateSystems.Vector(0, 0)
    assert sail.position == coordinateSystems.Vector(0, 0)

    sail.updatePosition(coordinateSystems.Vector(2, 0), 5)
    assert sail.velocity.x == 10
    assert sail.position.x == 25

def test_areaFacingSun():
    sail = spacecraft.SolarSail(1000, 1000, 45, coordinateSystems.Vector(960, 640))
    assert round(sail.areaFacingSun(), 3) == (sail.sailSize ** 2) / 2

def test_toPoint():
    sail = spacecraft.SolarSail(1000, 1000, 0, coordinateSystems.Sun.position)
    assert sail.toPoint(10) == (960, 590, 960, 490)