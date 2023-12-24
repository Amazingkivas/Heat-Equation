#pragma once

#include <iostream>
#include <functional>
#include <vector>

using std::function;
using BinaryFunction = function<double(double, double)>;
using UnaryFunction = function<double(double)>;
using std::vector;

class Grid {
private:
	vector<double> v;
	int n, m;	// Grid Sizes

public:
	Grid(int space_size = 1, int time_size = 1) : n(space_size), m(time_size) { v = vector<double>(n * m, 0.0); }

	double& operator() (int i, int j) {
		int index = i + j * n;
		return v[index];
	}

	int space_size() { return n; }
	int time_size() { return m; }
};

class RunThrough {
private:
	Grid v;			// Numerical solution
	double tau;		// Time Step
	double h;			// Space Step
	double Ai, Bi, Ci;	// Run-Through Coefficients
	int n, m;		// Grid Sizes
	double T;			// Maximum Time

	void initialize_parameters(UnaryFunction init_func, double gamma);
	void run(UnaryFunction boundary_functions[2], BinaryFunction g);

public:
	RunThrough(int sizes[2], double max_time, double coefficient,
		BinaryFunction source_function, UnaryFunction initial_function,
		double boundaries[2], UnaryFunction boundary_condtitions[2]) :
		n(sizes[0]), m(sizes[1]), T(max_time) {
		v = Grid(n + 1, m + 1);

		double left_boundary = boundaries[0];
		double right_boundary = boundaries[1];

		tau = T / static_cast<double>(m);
		h = (right_boundary - left_boundary) / static_cast<double>(n);
;
		initialize_parameters(initial_function, coefficient);
		run(boundary_condtitions, source_function);
	}

	Grid& get_whole_grid() { return v; }
};


void RunThrough::initialize_parameters(UnaryFunction init_func, double gamma) {
	for (int i = 0; i <= n; ++i) {
		v(i, 0) = init_func(static_cast<double>(i) * h);
	}
	Ai = Bi = (tau * gamma * gamma) / (h * h);
	Ci = 1.0 + (2.0 * tau * gamma * gamma) / (h * h);
}

void RunThrough::run(UnaryFunction boundary_functions[2], BinaryFunction g) {
	UnaryFunction mu1 = boundary_functions[0];
	UnaryFunction mu2 = boundary_functions[1];
	vector<double> alpha;
	vector<double> betta;
	double phi = 0.0;

	for (int j = 1; j <= m; j++) {
		// Фиктивные значения для корректировки индексов в соответствии с формулами
		// ------------------
		alpha.push_back(0.0);
		betta.push_back(0.0);
		// ------------------

		double t = static_cast<double>(j) * tau;

		// Прямой ход
		betta.push_back(mu1(t));
		alpha.push_back(0.0);
		for (int i = 1; i < n; i++) {
			alpha.push_back(Bi / (Ci - Ai * alpha[i]));
			double x = static_cast<double>(i) * h;
			phi = v(i, j - 1) + tau * g(x, t);
			betta.push_back((phi + Ai * betta[i]) / (Ci - alpha[i] * Ai));
		}

		// Обратный ход
		v(n, j) = mu2(t);
		for (int i = n - 1; i > 0; i--) {
			v(i, j) = alpha[i + 1] * v(i + 1, j) + betta[i + 1];
		}
		v(0, j) = mu1(t);

		betta.clear();
		alpha.clear();
	}
}
