import numpy as np
import matplotlib.pyplot as plt
import batman

#B filter fitting
tB, fluxB, dfluxB = np.loadtxt("B-data.csv", unpack=True, skiprows=1, usecols=[0, 1, 2], delimiter=',')


middle_indextB = int((len(tB) - 1) / 2)

tB = tB - tB[middle_indextB]  # - 0.025 + 0.01

plt.errorbar(tB*24, fluxB, yerr=dfluxB, fmt='o', label = 'B filter', color = 'red')
tV, fluxV, dfluxV = np.loadtxt("V-data.csv", unpack=True, skiprows=1, usecols=[0, 1, 2], delimiter=',')
fluxV = np.delete(fluxV, [0, 1])
dfluxV = np.delete(dfluxV, [0, 1])
tV = np.delete(tV, [0, 1])

middle_indextV = int((len(tV) - 1) / 2)

tV = tV - tV[middle_indextV]  # - 0.025 + 0.02

plt.errorbar(tV*24, fluxV, yerr=dfluxV, fmt='o', color='orange', label = "V filter")
params = batman.TransitParams()

a = np.arange(0.038, 0.051, 0.001)
rp = np.arange(1.3, 1.5, 0.02)
inc = np.arange(84, 90, 0.2)

uB = np.arange(0.65, 0.78, 0.01)
uV = np.arange(0.45, 0.78, 0.01)

offsetB = np.arange(0.005, 0.010, 0.001)
offsetV = np.arange(0.005, 0.010, 0.001)


def ModelLin(t, a, rp, inc, u, offset):
    p0 = 3.1
    params.t0 = 0.  # planet is exactly between the star and the observer
    params.per = p0  # orbital period
    params.inc = inc  # inclination in degrees
    params.ecc = 0.0  # eccentricity
    params.w = 0  # longitude in degrees
    params.u = [u]  # limb darkening coefficients
    params.limb_dark = "linear"  # limb darkening model

    params.rp = rp * 0.0921  # planet radius (stellar radii)
    params.a = a * 197.277  # semi-major axis (stellar radii)

    m = batman.TransitModel(params, t)
    flux_model = m.light_curve(params)
    return (np.array(flux_model) + offset)


def Chi2Lin(flux, t, a, rp, inc, u, offset, d):
    M = ModelLin(t, a, rp, inc, u, offset)
    X2 = np.sum(((flux - M) / d) ** 2)
    return X2



x2 = []



for i in range(len(a)):
    for j in range(len(rp)):
        for p in range(len(inc)):
                for n in range(len(uB)):
                    for m in range(len(offsetB)):
                        x2.append(Chi2Lin(fluxB, tB, a[i], rp[j], inc[p], uB[n], offsetB[m], dfluxB))

x2 = np.array(x2)
x2_matrica = np.reshape(x2, (len(a), len(rp), len(inc), len(uB), len(offsetB)))
index = np.argmin(x2_matrica)

ind1, ind2, ind3, ind4, ind5 = np.unravel_index(index, (len(a), len(rp), len(inc), len(uB),len(offsetB)))


plt.plot(tB*24, ModelLin(tB, a[ind1], rp[ind2], inc[ind3], uB[ind4], offsetB[ind5]), 'r')
plt.title("Light curve of Kepler-488 b transit (B filter)")
plt.xlabel("Transit duartion (hours)")
plt.ylabel("Relative flux")


print(a[ind1], rp[ind2], inc[ind3], uB[ind4], offsetB[ind5])

x2 = []


for i in range(len(a)):
    for j in range(len(rp)):
        for p in range(len(inc)):
                for n in range(len(uV)):
                    for m in range(len(offsetV)):
                        x2.append(Chi2Lin(fluxV, tV, a[i], rp[j], inc[p], uV[n], offsetV[m], dfluxV))

x2 = np.array(x2)
x2_matrica = np.reshape(x2, (len(a), len(rp), len(inc), len(uV), len(offsetV)))
index = np.argmin(x2_matrica)

ind1, ind2, ind3, ind4, ind5 = np.unravel_index(index, (len(a), len(rp), len(inc), len(uV),len(offsetV)))


plt.plot(tV*24, ModelLin(tV, a[ind1], rp[ind2], inc[ind3], uV[ind4], offsetV[ind5]), 'orange')
plt.title("Light curve of Kepler-488 b transit (B and V filter)")
plt.xlabel("Transit duration (hours)")
plt.ylabel("Relative flux")


print(a[ind1], rp[ind2], inc[ind3], uV[ind4], offsetV[ind5])

plt.legend()
plt.show()

