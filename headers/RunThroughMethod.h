#pragma once

#include <iostream>
#include <functional>
#include <vector>

using real = long double;
using std::function;
using std::vector;

class Grid {
private:
	vector<real> v;
	size_t n, m;	// Grid Sizes

public:
	Grid(size_t space_size = 1, size_t time_size = 1) : n(space_size), m(time_size) { v = vector<real>(n * m, 0.0); }

	real& operator() (size_t i, size_t j) {
		size_t index = i + j * n;
		return v[index];
	}

	size_t space_size() { return n; }
	size_t time_size() { return m; }
};

class RunThrough {
private:
	Grid v;			// Numerical solution
	real tau;		// Time Step
	real h;			// Space Step
	real Ai, Bi, Ci;	// Run-Through Coefficients
	size_t n, m;		// Grid Sizes
	real T;			// Maximum Time

	void initialize_parameters(function<real(real)> init_func, real gamma);
	void run(function<real(real)> boundary_functions[2], function<real(real, real)> g);

public:
	RunThrough(size_t sizes[2], real max_time, real coefficient, 
		function<real(real, real)> source_function, function<real(real)> initial_function,
		real boundaries[2], function<real(real)> boundary_condtitions[2]) : 
		n(sizes[0]), m(sizes[1]), T(max_time) {
		v = Grid(n + 1, m + 1);

		real left_boundary = boundaries[0];
		real right_boundary = boundaries[1];

		tau = T / static_cast<real>(m);
		h = (left_boundary - right_boundary) / static_cast<real>(n);
;
		initialize_parameters(initial_function, coefficient);
		run(boundary_condtitions, source_function);
	}

	Grid& get_whole_grid() { return v; }
};


void RunThrough::initialize_parameters(function<real(real)> init_func, real gamma) {
	for (size_t i = 0; i <= n; ++i) {
		v(i, 0) = init_func(static_cast<real>(i) * h);
	}
	Ai = Bi = (tau * gamma * gamma) / (h * h);
	Ci = 1.0 + (2.0 * tau * gamma * gamma) / (h * h);
}

void RunThrough::run(function<real(real)> boundary_functions[2], function<real(real, real)> g) {
	function<real(real)> mu1 = boundary_functions[0];
	function<real(real)> mu2 = boundary_functions[1];
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
