#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <gmp.h>
#include "trial.c"
#include "rho.c"
#include "ecm.c"

#define INITB1 2e3
#define INITB2 2e5
#define INITCURVES 16

// Liefert die Primfaktorzerlegung einer Zahl als String.
char *factorize(mpz_t number)
{
	// Primtest (Miller-Rabin).
	if (mpz_probab_prime_p(number, 10) > 0)
		return mpz_get_str(NULL, 10, number);

	mpz_t factor, cofactor;
	mpz_init(factor);
	mpz_init(cofactor);
	char *str1, *str2, *result;
	int B1 = INITB1, B2 = INITB2, curves = INITCURVES;

	// Zunaechst eine einfache Probedivision.
	trial(number, factor, 3e3);
	if (mpz_cmp_si(factor, 1) == 0)
	{
		// Zweite Strategie: Pollard-Rho.
		do
		{
			rho(number, factor, 4e4);
		} while (mpz_cmp(factor, number) == 0);
		// Falls immer noch kein Faktor gefunden wurde, mit ECM fortfahren.
		while (mpz_cmp_si(factor, 1) == 0)
		{
			ecm(number, factor, B1, B2, curves);
			if (mpz_cmp(factor, number) == 0)
			{
				mpz_set_si(factor, 1);
				B1 = INITB1;
				B2 = INITB2;
				curves = INITCURVES;
				continue;
			}
			// Anpassung der Parameter.
			B1 *= 4;
			B2 *= 5;
			curves = (curves * 5) / 2;
		}
	}

	mpz_divexact(cofactor, number, factor);
	str1 = factorize(factor);
	str2 = factorize(cofactor);
	result = (char *) malloc(strlen(str1) + strlen(str2) + 4);
	strcpy(result, str1);
	strcat(result, " * ");
	strcat(result, str2);

	mpz_clear(factor);
	mpz_clear(cofactor);
	return result;
}

// Das Hauptprogramm.
main(int argc, char *argv[])
{
	if (argc == 1)
	{
		printf("Wo ist die Eingabezahl?\n");
		return 1;
	}

	mpz_t number;
	mpz_init(number);

	if (mpz_set_str(number, argv[1], 10) == -1)
	{
		printf("Ungueltige Eingabe.\n");
		mpz_clear(number);
		return 1;
	}
	if (mpz_cmp_si(number, 2) < 0)
	{
		printf("Natuerliche Zahl > 1 erforderlich.\n");
		mpz_clear(number);
		return 1;
	}

	srand(time(0));
	printf("%s\n", factorize(number));
	mpz_clear(number);
	return 0;
}
