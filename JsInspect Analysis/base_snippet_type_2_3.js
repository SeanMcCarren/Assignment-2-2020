
getPrimes = function( N ) {
	let candidate = 1;
	let arr = [ 2 ];
	while ( arr.length < N ) {
		candidate += 2;
		let candidateIsShownComposite = false;
		for ( var j = 0; j < arr.length; j++ ) {
			if ( candidate % arr[ j ] == 0 ) {
				candidateIsShownComposite = true;
				break;
			}
		}
		if ( !candidateIsShownComposite ) {
			arr.push( candidate );
		}
	}
	return arr;
}

console.log( getPrimes(10) );
