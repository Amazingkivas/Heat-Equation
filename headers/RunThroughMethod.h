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
	size_t n, m;		// Grid Sizes

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
	Grid v;				// Numerical solution
	real tau;			// Time Step
	real h;				// Space Step
	real Ai, Bi, Ci;	// Run-Through Coefficients
	size_t n, m;		// Grid Sizes
	real T;				// Maximum Time

	void initialize_parameters(function<real(real)> init_func, real gamma);
	void run(function<real(real)> boundary_conditions[2], function<real(real, real)> g);

public:
	RunThrough(real left_boundary, real right_boundary, size_t space_size, size_t time_size, real max_time,
		function<real(real)> initial_function, real coefficient, function<real(real, real)> source_function,
		function<real(real)> left_boundary_condtition, function<real(real)> right_boundary_condtition) :
		n(space_size), m(time_size), T(max_time) {
		v = Grid(n + 1, m + 1);

		tau = T / static_cast<real>(m);
		h = (left_boundary - right_boundary) / static_cast<real>(n);

		function<real(real)> boundaries_array[2] = { left_boundary_condtition, right_boundary_condtition };
		initialize_parameters(initial_function, coefficient);
		run(boundaries_array, source_function);
	}

	Grid& get_whole_grid() { return v; }
};
