import numpy as np
import matplotlib.pyplot as plt

from Kinematics import leg_explicit_inverse_kinematics
from PupperConfig import *
from Gaits import *
from StanceController import position_delta, stance_foot_location
from SwingLegController import *
from Types import MovementReference, GaitParams, StanceParams, SwingParams
from Controller import *


def test_inverse_kinematics_linkage():
    print("""\n
    -------------- Testing Five-bar Linkage Inverse Kinematics -----------"""
    )
    config = PupperConfig()
    print("\nTesting Inverse Kinematics")

    def testHelper(r, alpha_true, i, do_assert=True):
        eps = 1e-6
        alpha = leg_explicit_inverse_kinematics(r, i, config)
        print("Leg ", i, ": r: ", r, " -> α: ", alpha)
        if do_assert:
            assert np.linalg.norm(alpha - alpha_true) < eps

    c = config.LEG_L / (2 ** 0.5)
    offset = config.ABDUCTION_OFFSET
    testHelper(np.array([0, offset, -0.125]), None, 1, do_assert=False)
    testHelper(np.array([c, offset, -c]), None, 1, do_assert=False)
    testHelper(np.array([-c, offset, -c]), None, 1, do_assert=False)
    testHelper(np.array([0, c, -c]), None, 1, do_assert=False)

    testHelper(np.array([-c, -offset, -c]), None, 0, do_assert=False)
    testHelper(
        np.array([config.LEG_L * (3 ** 0.5) / 2, offset, -config.LEG_L / 2]),
        None,
        1,
        do_assert=False,
    )


def test_stance_controller():
    print("\n-------------- Testing Stance Controller -----------")
    stanceparams = StanceParams()
    gaitparams = GaitParams()

    zmeas = -0.20
    mvref = MovementReference()
    dp, dR = position_delta(zmeas, stanceparams, mvref, gaitparams)
    assert np.linalg.norm(dR - np.eye(3)) < 1e-10
    assert np.linalg.norm(dp - np.array([0, 0, gaitparams.dt * 0.04])) < 1e-10

    zmeas = -0.18
    mvref = MovementReference()
    mvref.v_xy_ref = np.array([1.0, 0.0])
    mvref.z_ref = -0.18
    dp, dR = position_delta(zmeas, stanceparams, mvref, gaitparams)

    zmeas = -0.20
    mvref = MovementReference()
    mvref.wz_ref = 1.0
    mvref.z_ref = -0.20
    dp, dR = position_delta(zmeas, stanceparams, mvref, gaitparams)
    assert np.linalg.norm(dp - np.array([0, 0, 0])) < 1e-10
    assert np.linalg.norm(dR[0, 1] - (gaitparams.dt)) < 1e-6

    stancefootloc = np.zeros(3)
    sloc = stance_foot_location(stancefootloc, stanceparams, gaitparams, mvref)


def test_run():
    print("Run timing")
    foot_loc_history, joint_angle_history = run()
    plt.subplot(211)
    x = plt.plot(foot_loc_history[0, :, :].T, label="x")
    y = plt.plot(foot_loc_history[1, :, :].T, label="y")
    z = plt.plot(foot_loc_history[2, :, :].T, label="z")

    plt.subplot(212)
    alpha = plt.plot(joint_angle_history[0, :, :].T, label="alpha")
    beta = plt.plot(joint_angle_history[1, :, :].T, label="beta")
    gamma = plt.plot(joint_angle_history[2, :, :].T, label="gamma")
    plt.show()

    # plot(x, β, y, α, z, γ, layout=(3,2), legend=false))


test_inverse_kinematics_linkage()
test_stance_controller()
test_run()
