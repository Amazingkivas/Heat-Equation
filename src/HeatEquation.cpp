#include "HeatEquation.h"

bool Writer::write_grid(char* path) {
	std::ofstream fout;
	fout.open(path);
	if (!fout.is_open()) {
		std::cout << "ERROR: Failed to open Out File" << std::endl;
		return false;
	}
	for (size_t j = 0; j < _to_write.time_size(); ++j) {
		for (size_t i = 0; i < _to_write.space_size(); ++i) {

			fout << _to_write(i, j);
			if (i == _to_write.space_size() - 1) {
				fout << std::endl;
			}
			else {
				fout << ";";
			}
		}
	}
	fout.close();
	return true;
}

bool Writer::write_layer(char* path) {
	std::ofstream fout;
	fout.open(path);
	if (!fout.is_open()) {
		std::cout << "ERROR: Failed to open Out File" << std::endl;
		return false;
	}
	size_t n = _to_write.space_size() - 1;
	size_t m = _to_write.time_size() - 1;

	for (size_t i = 0; i <= n; ++i) {
		fout << _to_write(i, m);
		if (i < n) {
			fout << std::endl;
		}
	}
	fout.close();
	return true;
}
