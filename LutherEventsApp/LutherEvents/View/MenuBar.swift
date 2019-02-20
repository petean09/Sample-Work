//
//  MenuBar.swift
//  LutherEvents
//
//  Created by Anna Peterson on 1/14/19.
//  Copyright © 2019 Anna Peterson. All rights reserved.
//

import UIKit

// menubar is inside the navbar
class MenuBar: UIView, UICollectionViewDelegateFlowLayout, UICollectionViewDelegate, UICollectionViewDataSource {
    
    var horizontalBarLeftAnchorConstraint: NSLayoutConstraint?
    let cellId = "cellId"
    //array to add category text
    let categoryNames = ["All", "Athl", "Arts", "Other"]
    // gives access to homeController
    var homeController: HomeController?

    // customizatoin of menubar
    lazy var collectionView: UICollectionView = {
        let layout = UICollectionViewFlowLayout()
        let cv = UICollectionView(frame: .zero, collectionViewLayout: layout)
        // sets menu bar color
        cv.backgroundColor = UIColor.blue
        cv.dataSource = self
        cv.delegate = self
        return cv
    }()
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        
        collectionView.register(MenuCell.self ,forCellWithReuseIdentifier: cellId)
        
        addSubview(collectionView)
        addConstraintsWithFormat(format: "H:|[v0]|", views: collectionView)
        addConstraintsWithFormat(format: "V:|[v0]|", views: collectionView)
        
        // preselected "All" when app opens
        let selectedIndexPath = NSIndexPath(item: 0, section: 0)
        collectionView.selectItem(at: selectedIndexPath as IndexPath, animated: false, scrollPosition: UICollectionView.ScrollPosition.centeredHorizontally)
        
        // calls fuction to create small sliding white bar under menu
        setupHorizonalBar()
    }
    
    //creates the same horizontal bar, does not create movement tho
    func setupHorizonalBar() {
        let horizontalBarView = UIView()
        horizontalBarView.backgroundColor = UIColor.white
        horizontalBarView.translatesAutoresizingMaskIntoConstraints = false
        addSubview(horizontalBarView)
        
        // laying out view with constriants
        horizontalBarLeftAnchorConstraint = horizontalBarView.leftAnchor.constraint(equalTo: self.leftAnchor)
        horizontalBarLeftAnchorConstraint?.isActive = true
        horizontalBarView.bottomAnchor.constraint(equalTo: self.bottomAnchor).isActive = true
        horizontalBarView.widthAnchor.constraint(equalTo: self.widthAnchor, multiplier: 1/4).isActive = true
        horizontalBarView.heightAnchor.constraint(equalToConstant: 4).isActive = true
    }
    
    //creates movement of the small white horizontal bar
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        // this accesses the scrollToMenuIndex function from the HomeController
        // Allows the white bar to move on click of the pages button
        homeController?.scrollToMenuIndex(menuIndex: indexPath.item)
        
        // no need for animation anymore becuase it is take care by the HomeController in the scrollViewDidScroll function
        //print(indexPath.item)
//        let x = CGFloat(indexPath.item) * frame.width / 4
//        horizontalBarLeftAnchorConstraint?.constant = x
//
//        // animation of small white bar
//        UIView.animate(withDuration: 0.75, delay: 0, usingSpringWithDamping: 1, initialSpringVelocity: 1, options: .curveEaseOut, animations: self.layoutIfNeeded, completion: nil)
    }
    
    // 4 buttons
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 4
    }
    
    // creates cells where the buttons will be
    // with this method a cellId must be created and registered up above
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: cellId, for: indexPath) as! MenuCell // this down casts the cell so we can access the categorylabel
        
        cell.categoryLabel.text = (categoryNames[indexPath.item])
        return cell
    }
    
    // sizes cells to 1/4 of the menu bars width (there is a spacing issue between cells, next method mixes problem)
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: frame.width / 4, height: frame.height)
    }
    
    // fixes spacing issue
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 0
    }
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

class MenuCell: BaseCell {
    
    let categoryLabel: UILabel = {
        let cl = UILabel()
        //cl.text = "All"
        cl.textColor = UIColor.white
        cl.textAlignment = NSTextAlignment.center
        return cl
    }()
    
    // Anytime cell highlighted it changes to black
    override var isHighlighted: Bool {
        didSet { categoryLabel.textColor = isHighlighted ? UIColor.black : UIColor.white
        }
    }
    // Anytime cell selected it changes to black
    override var isSelected: Bool {
        didSet { categoryLabel.textColor = isSelected ? UIColor.black : UIColor.white
        }
    }
    
    override func setupViews() {
        super.setupViews()
        
        addSubview(categoryLabel)
        
        // gives height and width to menu cells
        addConstraintsWithFormat(format: "H:[v0(45)]", views: categoryLabel)
        addConstraintsWithFormat(format: "V:[v0(45)]", views: categoryLabel)
        
        // centers category text
        addConstraint(NSLayoutConstraint(item: categoryLabel, attribute: .centerX, relatedBy: .equal, toItem: self, attribute: .centerX, multiplier: 1, constant: 0))
        addConstraint(NSLayoutConstraint(item: categoryLabel, attribute: .centerY, relatedBy: .equal, toItem: self, attribute: .centerY, multiplier: 1, constant: 0))
    }
}
