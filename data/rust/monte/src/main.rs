use rand::prelude::*;
use std::time::Instant;
use std::thread;
use std::sync::{Mutex, Arc};
use std::fs;
use std::io::prelude::*;
use std::env;

 
struct Prob {
    label: String,
    weight: u32,
    prob: f32
}

#[derive(Clone)]
struct MonteResult {
    weight: u32,
    binaryStr: String
}


fn probDraw(pos: usize, allProb: &Vec<Prob>, mut rng: ThreadRng) -> u8 {
    let probInt: f32 = allProb[pos].prob;
    let randInt: f32 = rng.gen();
    if randInt <= probInt {
        return 1;
    }
    else {
        return 0;
    }
}
 
fn buildProbVector() -> Vec<Prob> {
    let mut probList: Vec<Prob> = Vec::new();
    //let path = env::current_dir();
    //println!("The current directory is {}", path.display());
    let data = fs::read_to_string("C:\\test\\data.txt").expect("Cannot read");
    let rows = data.split("\n");
    for row in rows {
        let cols: Vec<&str> = row.split(",").collect();
        let label: String = cols[0].to_string();
        let weight: u32 = cols[1].to_string().parse().unwrap();
        let prob: f32 = cols[2].to_string().trim_right().parse().unwrap();
        probList.push( Prob{ label: label, weight: weight, prob: prob }) ;
    }
    return probList;
    // return vec![
    //     Prob { weight: 10, prob: 0.7 },
    //     Prob { weight: 30, prob: 0.4 },
    //     Prob { weight: 40, prob: 0.6 },
    //     Prob { weight: 20, prob: 0.2 }
    // ];
}
 
fn runMonteTest(allProb: &Vec<Prob>, mut rng: ThreadRng) -> String  {
    let mut binStr: String = "".to_string();
    for n in (0..allProb.len()) {
        let test: u8 = probDraw(n, &allProb, rng);
        binStr = binStr + (if test == 0 {"0"} else {"1"});
    }
    return binStr;
}
 
fn getWeight(binStr: String, allProb: &Vec<Prob>) -> u32 {
    let mut weight: u32 = 0;
    for n in (0..binStr.len()) {
        if(binStr.chars().nth(n) == Some('1')) {
            weight = weight + allProb[n].weight
        }
    }
    return weight;
}
 
fn runFullMonte() -> Vec<MonteResult> {
    const runs : usize = 20000;
    //const runs : usize = 1000;
    let nthreads = 10;
    let mut results: Vec<MonteResult> = Vec::new();
    let mResults = Arc::new(Mutex::new(Vec::new()));
    // for n in (0..(iter)) {
    //     let mut rng = rand::thread_rng();
    //     //let binStr: String = "".to_string();
    //     let binStr: String = runMonteTest(&allProb, rng);
    //     results.push(getWeight(binStr, &allProb));
    // }
    let mut handles = vec![];
    for t in (0..nthreads) {
        let mResults = Arc::clone(&mResults);
        let handle = thread::spawn(move || {
            let tNum = t;
            let allProb: Vec<Prob> = buildProbVector();
            let mut rng = rand::thread_rng();
            for n in (0..(runs)) {
                //let binStr: String = "".to_string();
                let binStr: String = runMonteTest(&allProb, rng);
                let weight: u32 = getWeight(binStr.clone(), &allProb);
                let mut results = mResults.lock().unwrap();
                results.push( MonteResult{weight: weight, binaryStr: binStr.clone()} );
            }
        });
        handles.push(handle);
    }
    for handle in handles {
        handle.join().unwrap();
    }
    let finalResults = &*mResults.lock().unwrap();
    return finalResults.to_vec();
    //handle.join().unwrap();
    //return *mResults.lock().unwrap();
}

fn runFullMonteNT() -> Vec<MonteResult> {
    const runs : usize = 100000;
    let mut results: Vec<MonteResult> = Vec::new();
    let allProb: Vec<Prob> = buildProbVector();
    for n in (0..runs) {
        let mut rng = rand::thread_rng();
        //let binStr: String = "".to_string();
        let mut binStr: String = runMonteTest(&allProb, rng);
        let weight: u32 = getWeight(binStr.clone(), &allProb);
        results.push(MonteResult { weight: weight, binaryStr: binStr} );
    }
    return results;
}

fn recordResults(results: &Vec<MonteResult>) -> u8 {
    let mut contents = "".to_string();
    for result in results {
        let binStrList : Vec<&str> =  result.binaryStr.split("").collect();
        contents = contents + &(result.weight.to_string()) + "," + &binStrList.join(",") + "\n";
    }
    fs::write("C:\\test\\results.txt", contents).expect("Oh no");
    return 1;
}
 
fn main() {
    let before = Instant::now();
    let results = runFullMonte();
    recordResults(&results);
    println!("{0}", results.len());
    println!("{:.2?}", before.elapsed());
}