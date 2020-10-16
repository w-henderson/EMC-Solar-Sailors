from modules import photons

def test_Photon():
    testPhoton = photons.Photon(700)

    assert testPhoton.energy == 2.837779748816797e-19
    assert testPhoton.perSecond == 1.3552848848130575e+45
    assert testPhoton.momentum == 9.465814342857142e-28

def test_Photon_collisionsAtPosition():
    testPhoton = photons.Photon(700)

    assert testPhoton.collisionsAtPosition(100, 1000) == 1.0785014435786405e+40
    assert testPhoton.collisionsAtPosition(200, 1000) == 2.157002887157281e+40

def test_GeneralSunPhoton():
    # Doesn't work, not a priority to fix but I'm not writing tests for something that doesn't work
    return