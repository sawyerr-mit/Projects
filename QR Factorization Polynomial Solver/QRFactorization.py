import numpy as np

def companion_matrix(coeffs):
    coeffs = np.asarray(coeffs, dtype=float)

    if len(coeffs) < 2:
        raise ValueError("Polynomial must have degree >= 1.")

    coeffs = coeffs / coeffs[0]
    n = len(coeffs) - 1

    C = np.zeros((n, n))
    C[1:, :-1] = np.eye(n - 1)
    C[:, -1] = -coeffs[1:][::-1]

    return C

def QR_Algorithm(A):
    Ak = A.copy()
    for _ in range(1000):
        Q, R = np.linalg.qr(Ak)
        Ak = R @ Q
    return np.diag(Ak)

if __name__ == "__main__":
    coeffs = [1, -28, 322, -1960, 6769, -13132, 13068, -5040]
    C = companion_matrix(coeffs)

    np.set_printoptions(precision=0, suppress=True, floatmode='fixed')

    print("Coefficients:", coeffs)
    print("Companion matrix:\n", C)
    print("Eigenvalues:", QR_Algorithm(C))