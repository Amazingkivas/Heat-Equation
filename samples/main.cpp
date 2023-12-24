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

	double gamma = 2.0;
	auto g = [](double x, double t) { return exp(-1.0 * t) * sin(7.0 * M_PI * x) + 1.0; };
	auto phi = [](double x) { return 1.0 - x * x; };
	auto mu1 = [](double t) { return cos(t); };
	auto mu2 = [](double t) { return sin(4.0 * t); };
	double a = 0.0;
	double b = 1.0;

	function<double(double)> boundary_conditions_funcs[2] = { mu1, mu2 };
	double space_boundaries[2] = { a, b };

	HeatEquation eq(gamma, g, phi, space_boundaries, boundary_conditions_funcs);
	Grid solution;

	int n = static_cast<int>(numbers[0]);
	int m = static_cast<int>(numbers[1]);
	double T = static_cast<double>(numbers[2]);

	int sizes[2] = { n, m };
	solution = eq.solve_equation(T, sizes);
	double h = 1.0 / n;
	double tau = T / m;
	Writer write(solution, h, tau);
	
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
