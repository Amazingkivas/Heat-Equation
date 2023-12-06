#define _USE_MATH_DEFINES

#include <iostream>
#include <fstream>
#include <cmath>
#include "HeatEquation.h"
#include "RunThroughMethod.h"


int main(int argc, char* argv[]) {
	std::vector<double> numbers;
	std::ifstream source_fin;
	source_fin.open("Source.txt");
	if (!source_fin.is_open())
	{
		std::cout << "ERROR: Failed to open Source.txt" << std::endl;
		return 1;
	}
	double number;
	while (source_fin >> number)
	{
		numbers.push_back(number);
	}

	real gamma = 2.0;
	auto g = [](real x, real t) { return exp(-t) * sin(7 * M_PI * x) + 1; };
	auto phi = [](real x) { return 1 - x * x; };
	auto mu1 = [](real t) { return cos(t); };
	auto mu2 = [](real t) { return sin(4 * t); };
	real a = 0.0;
	real b = 1.0;

	function<real(real)> boundary_conditions_funcs[2] = { mu1, mu2 };
	real space_boundaries[2] = { a, b };

	HeatEquation eq(gamma, g, phi, space_boundaries, boundary_conditions_funcs);
	Grid solution;

	size_t n = static_cast<size_t>(numbers[0]);
	size_t m = static_cast<size_t>(numbers[1]);
	real T = static_cast<real>(numbers[2]);

	size_t sizes[2] = { n, m };
	solution = eq.solve_equation(T, sizes);
	Writer write(solution);
	
	if(!write.write_grid("OutputData.csv")) {
		std::cout << "ERROR: Failed to open OutputData.csv";
		return 1;
	}
	
	if (!write.write_layer("OutLayerData.txt")) {
		std::cout << "ERROR: Failed to open OutLayerData.txt";
		return 1;
	}

	source_fin.close();
	return 0;
}
