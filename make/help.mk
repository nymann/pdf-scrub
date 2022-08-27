help:
	@printf "\e[92m%s\e[0m\n" "make install"
	@echo " - Installs ${COMPONENT}."
	@printf "\e[92m%s\e[0m\n" "make install-all"
	@echo " - Install ${COMPONENT}, all development and tests dependencies in editable mode."
	@printf "\e[92m%s\e[0m\n" "make test"
	@echo " - Runs unit tests"
	@printf "\e[92m%s\e[0m\n" "make lint"
	@echo " - Lints your code (black, flake8 and mypy)."
	@printf "\e[92m%s\e[0m\n" "make fix"
	@echo " - Autofixes imports and some formatting."

.PHONY: help
.DEFAULT: help
