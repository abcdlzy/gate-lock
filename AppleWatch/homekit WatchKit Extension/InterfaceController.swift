//
//  InterfaceController.swift
//  homekit WatchKit Extension
//
//  Created by 李振宇 on 16/6/11.
//  Copyright © 2016年 李振宇. All rights reserved.
//

import WatchKit
import Foundation


class InterfaceController: WKInterfaceController {
    @IBOutlet var btnunlock: WKInterfaceButton!

    @IBOutlet var btnlock: WKInterfaceButton!
    
    @IBOutlet var lbtitle: WKInterfaceLabel!
    
    override func awakeWithContext(context: AnyObject?) {
        
        super.awakeWithContext(context)
        
        // Configure interface objects here.
    }
    internal override init() {
        let configuration = NSURLSessionConfiguration.defaultSessionConfiguration()
        session = NSURLSession(configuration: configuration);
    }
    
    let session: NSURLSession
    
    var data:String = ""

     func requestUrl(URL:String) {
        self.lbtitle.setText("发送指令中")
        let request = NSURLRequest(URL: NSURL(string: URL)!)
        let task = session.dataTaskWithRequest(request, completionHandler: { (data, response, error) -> Void in
            if error == nil {
                    self.lbtitle.setText("已成功发送指令")
            } else {
                dispatch_async(dispatch_get_main_queue(), { () -> Void in
                    self.lbtitle.setText(error?.description)
                })
            }
        })
        task.resume()
    }
    
    
    @IBAction func unlock() {
        requestUrl("http://192.168.31.68:8080/unlock")
        btnlock.setBackgroundColor(UIColor.brownColor())
        btnunlock.setBackgroundColor(UIColor.init(red: 0.1, green: 0.7, blue: 1, alpha: 1))
        let time: NSTimeInterval = 10.0
        let delay = dispatch_time(DISPATCH_TIME_NOW,
                                  Int64(time * Double(NSEC_PER_SEC)))
        dispatch_after(delay, dispatch_get_main_queue()) {
            self.btnunlock.setBackgroundColor(UIColor.brownColor())
            self.btnlock.setBackgroundColor(UIColor.init(red: 0.1, green: 0.7, blue: 1, alpha: 1))
            self.lbtitle.setText("门锁控制")
        }
        
    }

    @IBAction func lock() {
        requestUrl("http://192.168.31.68:8080/lock")
        btnlock.setBackgroundColor(UIColor.init(red: 0.1, green: 0.7, blue: 1, alpha: 1))
        btnunlock.setBackgroundColor(UIColor.brownColor())
        let time: NSTimeInterval = 5.0
        let delay = dispatch_time(DISPATCH_TIME_NOW,
                                  Int64(time * Double(NSEC_PER_SEC)))
        dispatch_after(delay, dispatch_get_main_queue()) {
            self.lbtitle.setText("门锁控制")
        }

    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
        super.willActivate()
        btnlock.setBackgroundColor(UIColor.init(red: 0.1, green: 0.7, blue: 1, alpha: 1))
        btnunlock.setBackgroundColor(UIColor.brownColor())
    }

    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
        super.didDeactivate()
    }

}
