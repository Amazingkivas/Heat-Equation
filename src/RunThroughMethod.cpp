#include "RunThroughMethod.h"

void RunThrough::initialize_parameters(function<real(real)> init_func, real gamma) {
	for (size_t i = 0; i <= n; ++i) {
		v(i, 0) = init_func(static_cast<real>(i) * h);
	}
	Ai = Bi = (tau * gamma * gamma) / (h * h);
	Ci = 1.0 + (2.0 * tau * gamma * gamma) / (h * h);
}

void RunThrough::run(function<real(real)> boundary_conditions[2], function<real(real, real)> g) {
	function<real(real)> mu1 = boundary_conditions[0];
	function<real(real)> mu2 = boundary_conditions[1];
	vector<real> alpha;
	vector<real> betta;
	real phi = 0.0;

	for (size_t j = 1; j <= m; ++j) {
		betta.push_back(mu1(static_cast<real>(j) * tau));
		alpha.push_back(0.0);

		v(0, j) = mu1(static_cast<real>(j) * tau);
		for (size_t i = 1; i <= n; ++i) {
			alpha.push_back(Bi / (Ci - Ai * alpha[i - 1]));
			phi = v(i, j - 1) + tau * g(static_cast<real>(i) * h, static_cast<real>(j) * tau);
			betta.push_back((phi + Ai * betta[i - 1]) / (Ci - alpha[i - 1] * Ai));
		}
		v(n, j) = mu2(static_cast<real>(j) * tau);

		for (size_t i = n - 1; i > 0; --i) {
			v(i, j) = alpha[i + 1] * v(i + 1, j) + betta[i + 1];
		}
		betta.clear();
		alpha.clear();
	}
}
