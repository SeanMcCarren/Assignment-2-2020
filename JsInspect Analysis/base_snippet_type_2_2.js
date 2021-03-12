
getPrimes = function( N ) {
	let c = 1;
	let arr = [ 2 ];
	while ( arr.length < N ) {
		c += 2;
		let candidateIsShownComposite = false;
		for ( var i = 0; i < arr.length; i++ ) {
			if ( c % arr[i] == 0 ) {
				candidateIsShownComposite = true;
				break;
			}
		}
		if ( !candidateIsShownComposite ) {
			arr.push( c );
		}
	}
	return arr;
}

console.log( getPrimes(10) );
