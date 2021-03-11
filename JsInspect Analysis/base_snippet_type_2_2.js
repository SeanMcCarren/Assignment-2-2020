
getPrimes = function( N ) {
	let candidate = 1;
	let a = [ 2 ];
	while ( a.length < N ) {
		candidate += 2;
		let candidateIsShownComposite = false;
		for ( var i = 0; i < a.length; i++ ) {
			if ( candidate % a[i] == 0 ) {
				candidateIsShownComposite = true;
				break;
			}
		}
		if ( !candidateIsShownComposite ) {
			a.push( candidate );
		}
	}
	return a;
}

console.log( getPrimes(10) );
