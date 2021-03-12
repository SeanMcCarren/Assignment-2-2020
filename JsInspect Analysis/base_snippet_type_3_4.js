
getPrimes = function( N ) {
	let candidate = 1;
	let arr = [ 2 ];
	while ( arr.length < N ) {
		candidate += 2;
		let candidateIsShownComposite = false;
		for ( var i = 0; i < arr.length; i++ ) {
			if ( candidate % arr[i] == 0 ) {
				candidateIsShownComposite = true;
			}
		}
		if ( !candidateIsShownComposite ) {
			arr.push( candidate );
		}
	}
	return arr;
}

console.log( getPrimes(10) );
