//
//  ViewController.swift
//  homekit
//
//  Created by 李振宇 on 16/6/11.
//  Copyright © 2016年 李振宇. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    func loadurl(url:String)->NSData? {
        
        let image_url:String = url
        let url:NSURL = NSURL(string:image_url)!

         return    NSData(contentsOfURL: url)!

        
        
    }
    
    @IBAction func lock(sender: AnyObject) {
        
        let data=loadurl("http://192.168.31.136:8080/unlock")
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

