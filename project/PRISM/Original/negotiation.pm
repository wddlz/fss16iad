dtmc

 //RESERVED PRICE - ACCEPTING INTERVAL [S_RP,B_RP]
// A player's RP characterises the certainty of refusal for a received proposal.
// any offer above(below) the RP is certainly rejected. 
// Buyer's and Seller's RPs give the accepting-interval [S_RP,B_RP] 
// We assume S_RP<B_RP
const int B_RP = 1000; // Buyer RESERVED_PRICE
const int S_RP = 1; // seller RESERVED_PRICE

// INITIAL PRICE
const int B_IP = S_RP; // Buyer Initial Price
const int S_IP = B_RP; // Seller Initial Price

// TIME-DEADLINE
// A player (b/s) offers its Reserved Price when it meets its time-deadline (Tb/Ts). 
// With a Boulware strategy, TbB(TsB) is the time at which a player starts conceding.
// Note: TbB(TsB) must be less than Tb(Ts).
const int Tb = 50; // Buyer Time-deadline
const int TbB =20; // Buyer start Conceding Time-deadline (for Boulware strat.)
const int Ts = 50; // Seller Time-deadline
const int TsB = 48; // Seller Time-deadline from which stops conceding (for Conceder strat.)

// BUYER INCREMENT, SELLER DECREMENT
// these values characterise Conceder and Boulware gradients for both players.
const int bCinc = 100;  // Buyer Conceder increment
const int bBinc = 1;   // Buyer Boulware increment
const int sCdec = 100;   // Seller Conceder decrement
const int sBdec = 1;   // Seller Boulware decrement

// SWITCHING FACTOR for Conceder strategy. 
// A player stops conceding when its next bid is less than Kb(Ks)*bCinc(sCdec) far 
// from the player's Reserved Price.
const int Kb = 1; // Buyer's switching factor
const int Ks = 8; // Seller's switching factor

// ACCEPTING INTERVAL'S OFFSET
// this value allows for considering a shifted   accepting interval [S_RP+Offset,B_RP+Offset] 
// while preserving model building's complexity (variables values are minimised 
// hence model's solution is simpler).
const Offset = 10000; // Offset for the accepting interval [S_RP+Offset,B_RP+Offset]

//  THE BUYER
module Buyer
	
	b:[0..6] init 0; 
	bid :[B_IP..B_RP] init B_IP;
	tb:[0..Tb] init 0; // bid counter
	Bcon : bool init false;
	Bstop : bool init false; 
	Bswitch :bool init false;
	Bagreed:bool init false;
	
	 // 0-  STRATEGY SWITCHING (pre Bid-Throwing)
	[] b=0 & !Bswitch & Bcon & B_RP-bid>Kb*bCinc -> 1 : (b'=1);
	[] b=0 & !Bswitch & !Bcon & tb<TbB -> 1 : (b'=1);
	[] b=0 & Bswitch -> 1 : (b'=1); 
	// Switch
	[] b=0 & !Bswitch & Bcon & B_RP-bid<=Kb*bCinc 
		-> 1 : (b'=1) & (Bcon'=false) & (Bswitch'=true); // CONCEDER to BOULWARE
	[] b=0 & !Bswitch & !Bcon & tb=TbB 
		-> 1 : (b'=1) & (Bcon'=true) & (Bswitch'=true); // BOULWARE to CONCEDER
	
	// 1- BID THROWING 
	[BID] b=1 & Sstop ->1 : (b'=4);
	[BID] b=1 & tb=0 & !Sstop -> 1 : (b'=6) & (tb'=tb+1); //starting bid
	
	[BID] b=1 & Bcon & tb>0 & tb<Tb-1 & B_RP-bid>bCinc & !Sstop  -> // CONCEDER
		1 : (b'=6) & (bid'=bid+bCinc) & (tb'=tb+1); //Conceding Increment
	[BID] b=1 & !Bcon & (tb>0 & tb<Tb-1) & (B_RP-bid)>bBinc & !Sstop -> // BOULWARE
		1 : (b'=6) & (bid'=bid+bBinc)& (tb'=tb+1); // Boulware Increment
	[BID] b=1 & tb>0 & Bcon & !Sstop & (tb=Tb-1 | B_RP-bid<=bCinc) -> 
		1 : (b'=6) & (bid'=B_RP) & (tb'=tb+1) & (Bstop'=true); // Last Bid reserved price
	[BID] b=1 & tb>0 & !Bcon & !Sstop & (tb=Tb-1 | B_RP-bid<=bBinc) -> 
		1 : (b'=6) & (bid'=B_RP) & (tb'=tb+1) & (Bstop'=true); // Last Bid reserved price
	
	// 6-  STRATEGY SWITCHING (post Bid-throwing)
	[] b=6  & !Bswitch & Bcon & B_RP-bid>Kb*bCinc  -> 1 : (b'=2);
	[] b=6  & !Bswitch & !Bcon & tb<TbB -> 1 : (b'=2); 
	[] b=6  & Bswitch -> 1 : (b'=2); 
	[] b=6  & !Bswitch & Bcon & B_RP-bid<=Kb*bCinc 
		-> 1 : (b'=2) & (Bcon'=false) & (Bswitch'=true); // CONCEDER to BOULWARE
	[] b=6  & !Bswitch & !Bcon & tb=TbB 
		-> 1 : (b'=2) & (Bcon'=true) & (Bswitch'=true); // BOULWARE to CONCEDER
	
	// 2- WAITING FOR BID ANALYSIS RESULT
	[] b=2 & s=2 -> 1 : (b'=3) & (Bagreed'=true);
	// 2- COUNTER-BID RECEIVING 
	[CBID] b=2 & !Bstop -> 1 : (b'=4);
	[CBID] b=2 & Bstop -> 1 : (b'=5);
	
	 // 3- AGREEMENT REACHED
	[PURCHASE] b=3  -> 1 : (b'=3);
	
	 // 4- COUNTER-BID ANALYSIS
	 // Conceder strategy
	[] b=4 & Bcon & tb<Tb-1 & bid+bCinc>=cbid  -> 1 : (b'=3);
	[] b=4 & Bcon & tb=Tb-1 & B_RP>=cbid -> 1 : (b'=3);
	[] b=4 & Bcon & !Sstop & ((tb<Tb-1 & bid+bCinc<cbid) | (tb=Tb-1 & B_RP<cbid)) ->
		    max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=3)
		+ 1-max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=0);
	[] b=4 & Bcon &  Sstop & ((tb<Tb-1 & bid+bCinc<cbid) | (tb=Tb-1 & B_RP<cbid)) -> 
		    max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=3)
		+ 1-max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=5);
	// Boulware strategy   
	[] b=4 & !Bcon & tb<Tb-1 & bid+bBinc>=cbid -> 1 : (b'=3);
	[] b=4 & !Bcon & tb=Tb-1 & B_RP>=cbid -> 1 : (b'=3) ;
	[] b=4 & !Bcon & !Sstop & tb<Tb-1 & bid+bBinc<cbid ->
		    max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=3)
		+ 1-max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=0);
	[] b=4 & !Bcon & (Sstop=true) & (tb<Tb-1) & ((bid+bBinc)<cbid)-> 
		    max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=3)
		+ 1-max(0,1 + (S_RP+Offset)/(cbid-(B_RP+S_RP+Offset))) : (b'=5);
	
	// 5- HALTING STATE 
	[STOP] b=5 -> 1 : (b'=5);
	
endmodule

// THE SELLER
module Seller

	s:[0..7] init 0;
	cbid :[S_RP..S_IP] init S_IP;
	ts:[0..Ts] init 0;     // cbid counter
	Scon: bool init true;
	Sstop: bool init false;
	Sswitch :bool init false;
	
	//  0- BID RECEIVING 
	[BID] s=0 & !Bstop & !Sstop -> 1 : (s'=1);
	[BID] s=0 & (Bstop | Sstop) -> 1 : (s'=5);
	// 1- BID ANALYSIS
	[] s=1 & Scon & cbid-sCdec<=bid -> 1 : (s'=2);
	[] s=1 & Scon & !Bstop & cbid-sCdec>bid 
		->  max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=2)
		+ 1-max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=6);
	[] s=1 & Scon & Bstop & cbid-sCdec>bid
		->  max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=2)
		+ 1-max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=5);
	[] s=1 & !Scon & ts<Ts-1 & cbid-sBdec<=bid -> 1 : (s'=2);
	[] s=1 & !Scon & ts=Ts-1 & cbid-sBdec<=bid -> 1 : (s'=2);
	[] s=1 & !Scon & !Bstop & cbid-sBdec>bid 
		->  max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=2)
		+ 1-max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=6);
	[] s=1 & !Scon & Bstop & cbid-sBdec>bid
		->  max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=2)
		+ 1-max(0,1-(S_RP+Offset)/(bid+Offset)) :(s'=5);
	
	// 2- AGREEMENT REACHED
	[PURCHASE] s=2 -> 1 : (s'=2);
	
	// 6- STRATEGY SWITCHING (pre CBID-throwing)
	[] s=6 & !Sswitch & Scon & cbid-S_RP>Ks*sCdec -> 1 : (s'=3);
	[] s=6 & !Sswitch & !Scon & ts<TsB -> 1 : (s'=3);
	[] s=6 & Sswitch -> 1 : (s'=3); 
	[] s=6 & !Sswitch & Scon & cbid-S_RP<=Ks*sCdec -> 
		1 : (s'=3) & (Scon'=false) & (Sswitch'=true); // CONCEDER to BOULWARE
	[] s=6 & !Sswitch & !Scon & ts=TsB ->
		1 : (s'=3) & (Scon'=true) & (Sswitch'=true); // BOULWARE to CONCEDER
	
	// 3- COUNTER-BID THROWING
	[CBID] s=3 & Bstop ->1 : (s'=5);
	[CBID] s=3 & ts=0 & !Bstop -> 1 : (s'=7) & (ts'=ts+1);
	[CBID] s=3 & Scon & !Bstop & ts>0 & ts<Ts-1 & cbid-S_RP>sCdec ->
		1 : (s'=7) & (cbid'=cbid-sCdec) & (ts'=ts+1);  // if Conceder stay Conceder
	[CBID] s=3 & !Scon & !Bstop  & ts>0 & ts<Ts-1 & cbid-S_RP>sBdec -> 
		1 : (s'=7) & (cbid'=cbid-sBdec) & (ts'=ts+1);  // if Conceder stay Conceder
	[CBID] s=3  & ts>0 & Scon & !Bstop & (ts=Ts-1 | cbid-S_RP<=sCdec) -> 
		1 : (s'=7) & (cbid'=S_RP) & (ts'=ts+1) & (Sstop'=true); // Last Bid reserved price
	[CBID] s=3  & ts>0 & !Scon & !Bstop & (ts=Ts-1 | cbid-S_RP<=sBdec) -> 
		1 : (s'=7) & (cbid'=S_RP) & (ts'=ts+1) & (Sstop'=true); // Last Bid reserved price
	
	// 4- WAITING FOR COUNTER-BID ANALYSIS RESULT
	[] s=4 & b=1 -> 1 : (s'=0);
	[] s=4 & b=3 -> 1 : (s'=2);
	
	// 5- HALTING STATE   
	[STOP] s=5 -> 1 : (s'=5);
	
	// 7- STRATEGY SWITCHING (post CBID-throwing)
	[] s=7 &  !Sswitch & Scon & cbid-S_RP>Ks*sCdec -> 1 : (s'=4);
	[] s=7 &  !Sswitch & !Scon & ts<TsB -> 1 : (s'=4); 
	[] s=7 &  Sswitch -> 1 : (s'=4); 
	[] s=7 & !Sswitch & Scon & cbid-S_RP<=Ks*sCdec ->
	 	 1 : (s'=4) & (Scon'=false) & (Sswitch'=true); // CONCEDER to BOULWARE
	[] s=7 & !Sswitch & !Scon & ts=TsB ->
	 	 1 : (s'=4) & (Scon'=true) & (Sswitch'=true); // BOULWARE to CONCEDER
	
endmodule
