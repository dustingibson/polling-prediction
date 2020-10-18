//use rust_decimal::Decimal;

// fn nCr(n:u32, r:u32) -> Decimal {
//     return f(n) / 
// }

use factorial::Factorial;

fn nCr(n:u128, r:u128) -> u128 {
    let diff:u128 = n - r;
    return n.factorial() / (diff.factorial() * r.factorial());
}


fn main() {
    //let n: u64 = nCr(5u128,3u128);
    let n: u128 = nCr(10u128, 3u128);
    println!("{0}",n);
}