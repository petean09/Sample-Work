//
//  Extensions.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/14/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

// adds constraints easier than writing them all out
extension UIView {
    func addConstraintsWithFormat(format: String, views: UIView...) {
        var viewsDictionary = [String: UIView]()
        for (index, view) in views.enumerated() {
            let key = "v\(index)"
            view.translatesAutoresizingMaskIntoConstraints = false
            viewsDictionary[key] = view
        }
        
        addConstraints(NSLayoutConstraint.constraints(withVisualFormat: format, options: NSLayoutConstraint.FormatOptions(), metrics: nil, views: viewsDictionary))
        
    }
}
// Since View Controller is embedded in the Navigation Controller this is used to tell the app the update
extension UINavigationController {
    override open var preferredStatusBarStyle : UIStatusBarStyle {
        return topViewController?.preferredStatusBarStyle ?? .default
    }
}

