
getPrimes = function(N) { /* Classic prime seive*/ /* Initialization*/ let candidate = 1; /* Candidate prime*/let arr = [2]; /* Array of primes*/while (arr.length < N) {candidate += 2; candidateIsShownComposite = false; /*Becomes TRUE if we know candidate is not prime*/ for (var i = 0; i < arr.length; i++) {/* Assume arr correctly contains all primes up until candidate. Then if candidate is divisible by any of these primes, candidate is not prime */ if (candidate % arr[i] == 0) { let candidateIsShownComposite = true; break; } } if  (!candidateIsShownComposite) { arr.push(candidate); } } /* Return the array */ return arr; }

console.log(getPrimes(10))
