// Needs:   3 x M2.5x14mm bolt
//          3 x M2.5 nuts
//
// Resin: 0-7 No support, anti aliasing=smooth surfaces, high definition ant-aliasing
// TPU 95A: 8 No support, 25% fill  

partNum                 = 0;    // 0 = All, 1 = Case, 2 = Buttons, 3 = Bottom Case, 4 = Top Case, 5 = GPS Washer, 6 = Knob, 7 = LED Holder, 8 = Support Band

splitCase               = true;
caseSideBorder          = 2.0;
caseBottomBorder        = 3.0;
caseTopBorder           = 1.0;
caseRadius              = 2.5;
splitOffsetZ            = 16.0;
caseInnerDimensions     = [68.0, 32.0 + 6.0 * 2, 10.5 + splitOffsetZ];
caseOuterDimensions     = caseInnerDimensions + [caseSideBorder * 2, caseSideBorder * 2, caseBottomBorder + caseTopBorder];

pcbBaseHeight           = 9.0;

caseSplitHeight         = caseBottomBorder + 4.4 + splitOffsetZ;

manifoldCorrection      = 0.01;

holeUsbCDimensions      = [caseSideBorder + manifoldCorrection * 2, 9.4, 3.6];
holeUsbCPos             = [-caseInnerDimensions[0]/2 + manifoldCorrection, 0, caseSplitHeight];

pcbBoardClearance       = 0.05;
pcbBoardThickness       = 1.6;

boltDiameter            = 2.7;
boltHeadDiameter        = 4.9;
boltHeadHeight          = 1.7;
nutDiameter             = 6.1;
nutThickness            = 2.0;

pcbPostBottomDiameter   = 5.0;
pcbPostTopDiameter      = 3.5;
pcbPostReinforceDiameter= 7.6;
pcbPostNutRecess        = 6.0;
pcbPostReinforceHeight  = pcbPostNutRecess - caseBottomBorder + 2;
pcbBoltHeight           = caseBottomBorder + pcbBaseHeight + pcbBoardThickness + boltHeadHeight;
pcbTopPostHeight        = 2.85;

casePostBottomDiameter  = 5.0;
casePostReinforceDiameter= 7.6;
casePostNutRecess       = 20.5;
casePostReinforceHeight = casePostNutRecess + 2;
caseBoltHeight          = caseOuterDimensions[2];
casePostsXY             = [[-(caseInnerDimensions[0]/2 - 2.5), -(caseInnerDimensions[1]/2 - 2.5)],
                           [-(caseInnerDimensions[0]/2 - 2.5),  (caseInnerDimensions[1]/2 - 2.5)],
                           [ (caseInnerDimensions[0]/2 - 2.5), -(caseInnerDimensions[1]/2 - 2.5)],
                           [ (caseInnerDimensions[0]/2 - 2.5),  (caseInnerDimensions[1]/2 - 2.5)]]; 

pcbMountingLocationsXY  = [[-caseInnerDimensions[0]/2 + 3.0,  17.8/2],
                           [-caseInnerDimensions[0]/2 + 3.0, -17.8/2],
                           [-caseInnerDimensions[0]/2 + 3.0 + 45.5,  17.8/2.0],
                           [-caseInnerDimensions[0]/2 + 3.0 + 45.5, -17.8/2.0]];

lcdHoleDimensions       = [28.0, 17.2];
lcdHolePosXY            = [-caseInnerDimensions[0]/2 + 11.7, 0];

buttonHoleDimensions    = [5.0, 4.0];
buttonD0HolePosXY       = [-caseInnerDimensions[0]/2 + 8.0, -7.0];
buttonD1HolePosXY       = [-caseInnerDimensions[0]/2 + 8.0, 0.0];
buttonD2HolePosXY       = [-caseInnerDimensions[0]/2 + 8.0, 7.0];
buttonResetHolePosXY    = [-caseInnerDimensions[0]/2 + 45.0, 0.0];

cubeDimXY               = [caseOuterDimensions[0] + manifoldCorrection * 2, caseOuterDimensions[1] + manifoldCorrection * 2];

ventsXYMin              = [-24, -17];
ventsXYMax              = [9, 18];
ventsDistance           = 2.5;
ventsDiameter           = 1.5;

buttonMainDimensions    = [buttonHoleDimensions[0] - 0.5, buttonHoleDimensions[1] - 0.5];
buttonMainHeight        = 2.8;
legLongWidth            = 0.8;
legLongLength           = buttonMainDimensions[0] + 0.3 + 2.0;
legShortWidth           = 1.5;
legShortLength          = buttonMainDimensions[1] + 0.3 + 2.0;
legThickness            = 0.5;
buttonLozenge           = [3.8, 3.0, 0.5];
buttonCornerDimensions  = [2.0, 2.0, 0.8];

potHoleDiameter         = 8.0;
potHoleXY               = [25.6525, -6.985];

gpsHoleDiameter         = 7.0;
gpsHoleOffsetY          = -11.5;
gpsHoleOffsetZ          = 18.5;

wireHoleLength          = 3.35;
wireHoleDepth           = 1.68;
wireHoleY               = 7.0;

logoPosXY               = [0, 17];
textDepth               = 0.5;
D0PosXY                 = [-32.25, 10];
D1PosXY                 = [-32.65, 3];
D2PosXY                 = [-32.25, -4];
ResetPosXY              = [16, 8.5];
PlusPosXY               = [potHoleXY[0] + 6, potHoleXY[1] + 10];
MinusPosXY              = [potHoleXY[0] + 6, potHoleXY[1] - 9];

knobOutsideDiameter     = 18.8;
knobHeight              = 13.0;
knobInsideDiameter      = 6.2;
knobTopThickness        = 1.0;
knobIndentDiameter      = 2.5;
knobMarkerWidth         = 1;
knobMarkerDepth         = 0.5;
knobScrewDepth          = 5.0;
knobScrewDiameter       = 3.0;
knobNutDiameter         = 6.2;
knobNutThickness        = 2.5;
knobNutShaftWidth       = 5.55;
knobNutOffset           = -3.5;
knobBoltHeadDiameter    = 6.0;
knobBoltHeadHeight      = 1.8;
knobHeadOffset          = knobNutOffset - knobNutThickness - 0.5;

gpsWasherDimensions     = [6.0, 3.0, 2.4];


ledLegBorderThickness   = 2.0;
ledLegCoverThickness    = 2.0;
ledLegCoverClearance    = 0.2;
ledLegCoverDepthBelowTop= 0.5;
ledLegPostHeight        = 5.5;
ledLegCoverPostHeight   = 2.5;

ledLegDimensions        = [60, 17.5 + ledLegBorderThickness * 2, ledLegBorderThickness + ledLegPostHeight + pcbBoardThickness + ledLegCoverPostHeight + ledLegCoverThickness + ledLegCoverDepthBelowTop];  

ledLegInnerDimensions   = [ledLegDimensions[0] - ledLegBorderThickness, ledLegDimensions[1] - ledLegBorderThickness * 2, ledLegDimensions[2] - ledLegBorderThickness];  

ledLegCoverDimensions   = [ledLegInnerDimensions[0] - ledLegCoverClearance, ledLegInnerDimensions[1] - ledLegCoverClearance * 2, ledLegCoverThickness];

ledLegCoverLugDimensions= [ledLegBorderThickness / 2, 2.0, ledLegCoverThickness];
ledLegCoverLugPosY      = 5;
ledLegDiameter          = 5.2;
ledLegLedPosX           = 3.429;
ledLegHolesPos1XY       = [4.191 + ledLegLedPosX, -5.42925];
ledLegHolesPos2XY       = [3.556 + ledLegLedPosX, 5.36575];
ledLegPostDiameter      = 6.75;
ledLegCoverPostDiameter = 4.0;
ledLegBoltRecess        = 3.6;

magnetDiameter          = 10.5;
magnetThickness         = 3.2;

legSupportDimensions    = [100, ledLegDimensions[1] + 4 * 2, magnetThickness + 1.0];
legSupportScrewHoleDiameter     = 5.0;
legSupportScrewHoleOffsetX      = 20;

legSupportCutoutDimensions      = [ledLegDimensions[2] / 2, ledLegDimensions[1] + 0.3 * 2, legSupportDimensions[2] + manifoldCorrection * 2];
legSupportRetainerDimensions    = [7, legSupportDimensions[1] + 5 * 2, legSupportDimensions[2]];
legSupportRetainerOffsetX       = -42;
legSupportRetainerCutoutDiameter= 3.0;
legSupportRetainerCutoutOffsetY = legSupportRetainerDimensions[1]/2 - 3.5; 

supportBandThickness            = 2.0;
supportBandLengthReduction      = 1.0;
supportBandBorder       = 2.0;


adafruitOffsetY         = 3.14325;

splitCaseOffset         = 3;
    
use <PoetsenOne-Regular.ttf>

$fn                     = 40;


if ( partNum == 0 || partNum == 1 )
{
    if ( splitCase )
        splitCase(0);
    else
        case();
}

if ( partNum == 0 || partNum == 2 )
{
    translate( [-53, 1, 0] )
        buttons();
    translate( [-45, 1, 0] )
        buttons();
}

if ( partNum == 0 || partNum == 3 )
{
    if ( splitCase )
        splitCase(-1);
}

if ( partNum == 0 || partNum == 4 )
{
    if ( splitCase )
        splitCase(1);
}

if ( partNum == 0 || partNum == 5 )
{
    translate( [-39.5, 21, 0] )
        donut(gpsWasherDimensions[0], gpsWasherDimensions[1], gpsWasherDimensions[2]);
    translate( [-39.5, 13, 0] )
        donut(gpsWasherDimensions[0], gpsWasherDimensions[1], gpsWasherDimensions[2]);
}

if ( partNum == 0 || partNum == 6 )
{
    translate( [-47, -14, knobHeight] )
        rotate( [180, 0, 0] )
            knob();
}

if ( partNum == 7 )
{
    translate( [49, 20, 0] )
        ledHolder();
}

if ( partNum == 8 )
{
    translate( [75, 56, 0] )
        supportBand();
}



module supportBand()
{
    supportBandInnerDimensions = [legSupportRetainerDimensions[0] * 2 + ledLegDimensions[2] * 2 + ledLegDimensions[1] - supportBandLengthReduction, legSupportRetainerDimensions[2], supportBandThickness]; 
    
    translate( [0, 0, supportBandInnerDimensions[2]/2] )
    {
        difference()
        {
            cube( supportBandInnerDimensions + [supportBandBorder * 2, supportBandBorder * 2, 0], center = true);
            cube( [supportBandInnerDimensions[0], supportBandInnerDimensions[1], supportBandInnerDimensions[2] + manifoldCorrection * 2], center = true);
        }
    }
}


module ledHolder()
{
    //90 degree holder has screwholes and magnets in the center and 2 hooks for rubber band
    // Cover latches at front end 1mm down
    
    // Main Leg
    translate( [0, 0, ledLegDimensions[2]] )
        rotate( [180, 0, 0] )
            difference()
            {
                union()
                {
                    difference()
                    {
                        // Main Body
                        union()
                        {
                            translate( [0, -ledLegDimensions[1]/2, 0] )
                                cube( ledLegDimensions );
        
                            cylinder(d = ledLegDimensions[1], h = ledLegDimensions[2]); 
                        }
        
                        // Inset
                        translate( [0, 0, -manifoldCorrection] )
                        {   
                            translate( [0, -ledLegInnerDimensions[1]/2, -manifoldCorrection] )
                                cube( [ledLegInnerDimensions[0], ledLegInnerDimensions[1], ledLegInnerDimensions[2] + manifoldCorrection] );

                            cylinder(d = ledLegInnerDimensions[1], h = ledLegInnerDimensions[2] + manifoldCorrection);
                        }
                    }
               
                    // Posts
                    translate( [0, 0, ledLegDimensions[2] - ledLegBorderThickness - ledLegPostHeight] )
                    {
                        translate( [ledLegHolesPos1XY[0], ledLegHolesPos1XY[1], 0] )
                            cylinder(d = ledLegPostDiameter, h = ledLegPostHeight);
                        translate( [ledLegHolesPos2XY[0], ledLegHolesPos2XY[1], 0] )
                            cylinder(d = ledLegPostDiameter, h = ledLegPostHeight);
                    }
                }
        
                // Wire Hole
                translate( [ledLegDimensions[0] - ledLegBorderThickness - manifoldCorrection, -wireHoleLength/2, -manifoldCorrection] )
                    cube( [ledLegBorderThickness + manifoldCorrection * 2, wireHoleLength, wireHoleDepth + ledLegCoverThickness + ledLegCoverDepthBelowTop + manifoldCorrection] );
         
                // Lugs Holes
                translate( [ledLegCoverDimensions[0], -ledLegCoverLugDimensions[1]/2, ledLegCoverDepthBelowTop] )
                {
                    translate( [0 , ledLegCoverLugPosY, 0] )
                        cube( ledLegCoverLugDimensions + [ledLegCoverClearance * 2, ledLegCoverClearance * 2, ledLegCoverClearance * 2] );
                    translate( [0, -ledLegCoverLugPosY, 0] )
                        cube( ledLegCoverLugDimensions +  [ledLegCoverClearance * 2, ledLegCoverClearance * 2, ledLegCoverClearance * 2] );
                }
        
                // LED Hole
                translate( [ledLegLedPosX, 0, ledLegDimensions[2] - ledLegBorderThickness - manifoldCorrection] )
                    cylinder(d = ledLegDiameter, h = ledLegBorderThickness + manifoldCorrection * 2);
            
                // Bolt Holes
                ledLegBoltHoles();
            }
    
    
    // Cover
    translate( [0, 21, 0] )
    {
        difference()
        {
            union()
            {
                // Cover
                translate( [0, -ledLegCoverDimensions[1]/2, 0] )
                    cube( [ledLegCoverDimensions[0], ledLegCoverDimensions[1], ledLegCoverDimensions[2]] );

                cylinder(d = ledLegCoverDimensions[1], h = ledLegCoverDimensions[2]);   
   
                // Lugs
                translate( [ledLegCoverDimensions[0], -ledLegCoverLugDimensions[1]/2, 0] )
                {
                    translate( [0, ledLegCoverLugPosY, 0] )
                        cube( ledLegCoverLugDimensions );
                translate( [0, -ledLegCoverLugPosY, 0] )
                        cube( ledLegCoverLugDimensions );
                }
        
                // Lug Wire Cover
                translate( [ledLegDimensions[0] - ledLegCoverClearance - ledLegBorderThickness  - manifoldCorrection, -(wireHoleLength-ledLegCoverClearance)/2, 0] )
                    cube( [ledLegBorderThickness + ledLegCoverClearance + manifoldCorrection * 2, wireHoleLength - ledLegCoverClearance, ledLegCoverThickness] );

                // Posts
                translate( [0, 0, ledLegCoverThickness] )
                {
                    translate( [ledLegHolesPos1XY[0], ledLegHolesPos1XY[1], 0] )
                        cylinder(d = ledLegCoverPostDiameter, h = ledLegCoverPostHeight);
                    translate( [ledLegHolesPos2XY[0], ledLegHolesPos2XY[1], 0] )
                        cylinder(d = ledLegCoverPostDiameter, h = ledLegCoverPostHeight);
                }
            }
         
            translate( [0, 0, -ledLegCoverDepthBelowTop] )
                ledLegBoltHoles();
        }
    }
    
    // Leg Support
    translate( [40, -27, 0] )
        rotate( [0, 0, 180] )
        {
            difference()
            {
                union()
                {
                    translate( [0, 0, legSupportDimensions[2]/2] )
                        cube( legSupportDimensions, center = true );
                    
                    translate( [legSupportRetainerOffsetX, -legSupportRetainerDimensions[1]/2, 0] )
                        cube( legSupportRetainerDimensions );
                }
            
                translate( [legSupportRetainerOffsetX + legSupportRetainerDimensions[0], 0, -manifoldCorrection] )
                {
                    translate( [0, -legSupportRetainerCutoutOffsetY, 0] )
                        cylinder(d = legSupportRetainerCutoutDiameter, h = legSupportDimensions[2] + manifoldCorrection * 2);
                    translate( [0, legSupportRetainerCutoutOffsetY, 0] )
                        cylinder(d = legSupportRetainerCutoutDiameter, h = legSupportDimensions[2] + manifoldCorrection * 2);
                }
                
                // Magnet hole
                translate( [0, 0, legSupportDimensions[2] - magnetThickness] )
                    cylinder(d = magnetDiameter, h = magnetThickness + manifoldCorrection);

                // Screw Holes
                translate( [-legSupportScrewHoleOffsetX, 0, -manifoldCorrection] )
                    cylinder(d = legSupportScrewHoleDiameter, h = legSupportDimensions[2] + manifoldCorrection * 2);
                translate( [legSupportScrewHoleOffsetX, 0, -manifoldCorrection] )
                    cylinder(d = legSupportScrewHoleDiameter, h = legSupportDimensions[2] + manifoldCorrection * 2);
                    
                // Leg support cutout
                translate( [-legSupportDimensions[0] / 2 - manifoldCorrection, -legSupportCutoutDimensions[1] / 2, -manifoldCorrection] )
                    cube( legSupportCutoutDimensions );
            }
        }
}


module ledLegBoltHoles()
{
    boltLength = ledLegDimensions[2] - ledLegCoverDepthBelowTop;

    translate( [0, 0, boltLength + ledLegCoverDepthBelowTop] )
    {
        translate( [ledLegHolesPos1XY[0], ledLegHolesPos1XY[1], 0] )
            rotate( [0, 180, 0] )
                boltNut(boltLength, boltHeadDiameter, boltDiameter, boltHeadHeight, nutDiameter, ledLegBoltRecess);
        translate( [ledLegHolesPos2XY[0], ledLegHolesPos2XY[1], 0] )
            rotate( [0, 180, 0] )
                boltNut(boltLength, boltHeadDiameter, boltDiameter, boltHeadHeight, nutDiameter, ledLegBoltRecess);
    }
}


module knob()
{
    difference()
    {
        union()
        {
            donut(knobOutsideDiameter, knobInsideDiameter, knobHeight - knobTopThickness, $fn = 80);
            translate( [0, 0, knobHeight - knobTopThickness] )
                cylinder(d=knobOutsideDiameter, h=knobTopThickness, $fn = 80);
        }
        
        // Knurl
        for ( rot = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330] )
        {
            rotate( [0, 0, rot] )
                translate( [-knobOutsideDiameter/2, 0, -manifoldCorrection] )
                    cylinder(d = knobIndentDiameter, h = knobHeight + manifoldCorrection * 2);
        }
        
        // Marker
        translate( [-knobOutsideDiameter/4, 0, knobHeight - knobMarkerDepth/2] )
            cube( [knobOutsideDiameter/2, knobMarkerWidth, knobMarkerDepth + manifoldCorrection], center = true );
            
        // Screw Hole
        translate( [0, 0, knobScrewDepth] )
            rotate( [90, 0, 270] )
                cylinder(d = knobScrewDiameter, h = knobOutsideDiameter/2 + manifoldCorrection);
        
        // Nut hole and channel
        translate( [knobNutOffset, 0, 0] )
        {
            // Nut
            translate( [0, 0, knobScrewDepth] )
                rotate( [90, 30, 270] )
                    cylinder(d = knobNutDiameter, h = knobNutThickness, $fn=6);
        
            // Shaft
            rotate( [0, 0, 180] )
                translate( [0, -knobNutShaftWidth/2, -manifoldCorrection] )
                    cube( [knobNutThickness, knobNutShaftWidth, knobScrewDepth + manifoldCorrection] );
        }
        
        translate( [knobHeadOffset, 0, knobScrewDepth] )
            rotate( [0, 270, 0] )
            {
                cylinder(d2 = knobBoltHeadDiameter, d1 = knobScrewDiameter, h = knobBoltHeadHeight);
                translate( [0, 0, knobBoltHeadHeight - manifoldCorrection] )
                    cylinder(d = knobBoltHeadDiameter, h = 5);
            }
    }
}



module buttons()
{
    button();
    translate( [0, 8, 0] )
        button();
    translate( [0, 16, 0] )
        button();
    translate( [0, 24, 0] )
        button();     
}



module button()
{
    difference()
    {
        union()
        {
            translate( [0, 0, legThickness/2] )
            {
                cube( [legLongLength, legLongWidth, legThickness], center = true );
                cube( [legShortWidth, legShortLength, legThickness], center = true );
                cube( [1.2, 9, legThickness], center = true);
            }
   
            translate( [0, 0, buttonMainHeight/2] )
                cube( [buttonMainDimensions[0], buttonMainDimensions[1], buttonMainHeight], center = true);
        }
        
        translate( [0, 0, -manifoldCorrection] )
            lozenge( buttonLozenge[0], buttonLozenge[1], buttonLozenge[2] + manifoldCorrection );
            
        for ( posXY = [[buttonMainDimensions[0]/2, buttonMainDimensions[1]/2, 0, -45], [-buttonMainDimensions[0]/2, buttonMainDimensions[1]/2, 45, 0], [buttonMainDimensions[0]/2, -buttonMainDimensions[1]/2, -45, 0], [-buttonMainDimensions[0]/2, -buttonMainDimensions[1]/2, 0, 45]] )
            translate( [posXY[0], posXY[1], buttonCornerDimensions[2]/2 - manifoldCorrection] )
                rotate( [posXY[2], posXY[3], 45] )
                    cube( buttonCornerDimensions, center = true);
    }
}



module splitCase(parts)
{
    cubeOriginXY = [-cubeDimXY[0] / 2, -cubeDimXY[1]];
    
    if ( parts == 0 || parts == 1 )
        translate( [0, cubeDimXY[1] + splitCaseOffset, caseSplitHeight + caseOuterDimensions[2] - caseSplitHeight] )
            rotate( [ 180, 0, 0] )
                difference()
                {
                    case();
                    translate( [cubeOriginXY[0], cubeOriginXY[1] / 2, -manifoldCorrection] )
                        cube([cubeDimXY[0], cubeDimXY[1], caseSplitHeight + manifoldCorrection]);
                }
    
    if ( parts == 0 || parts == -1 )
        difference()
        {
            case();
            translate( [cubeOriginXY[0], cubeOriginXY[1] / 2
            , caseSplitHeight] )
                cube([cubeDimXY[0] * 2, cubeDimXY[1], caseOuterDimensions[2] - caseSplitHeight + manifoldCorrection]);
        }
}



module case()
{
    difference()
    {
        union()
        {
            difference()
            {
                roundedCube(caseOuterDimensions, caseRadius);
        
                translate( [0, 0, caseBottomBorder] )
                    roundedCube(caseInnerDimensions, caseRadius);
                    
                                
                // Logo
                translate( [logoPosXY[0], logoPosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("Stamp Of Approval", size=4.5, font="PoetsenOne", spacing=1.0, halign="center", valign="center");

                // Buttons
                translate( [D0PosXY[0], D0PosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("D0", size=4.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");
                
                translate( [D1PosXY[0], D1PosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("D1", size=4.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");
                
                translate( [D2PosXY[0], D2PosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("D2", size=4.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");
 
                 translate( [ResetPosXY[0], ResetPosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("Reset", size=4.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");

                 translate( [PlusPosXY[0], PlusPosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("+", size=5.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");
       
                 translate( [MinusPosXY[0], MinusPosXY[1], caseOuterDimensions[2] - textDepth + manifoldCorrection] )
                    linear_extrude(textDepth + manifoldCorrection)
                        text("-", size=5.0, font="PoetsenOne", spacing=1.0, halign="center", valign="center");
            }
                            
            translate( [0,  adafruitOffsetY, 0] )
                postsPCBTop();    
            postsPCBBottom();
        }
        
        translate( [0, adafruitOffsetY, 0] )
        {
            // USB C Hole
            translate( holeUsbCPos )
                rotate( [90, 0, 270] )
                    lozenge(holeUsbCDimensions[1], holeUsbCDimensions[2],holeUsbCDimensions[0]);

            caseTopBorderOffset = caseOuterDimensions[2] - caseTopBorder - manifoldCorrection;

            // lcd hole
            translate( [lcdHolePosXY[0], -lcdHoleDimensions[1]/2 + lcdHolePosXY[1], caseTopBorderOffset] )
                cube( [lcdHoleDimensions[0], lcdHoleDimensions[1], caseTopBorder + manifoldCorrection * 2] );
            
            // button holes D0/D1/D2
            for ( posXY = [buttonD0HolePosXY, buttonD1HolePosXY, buttonD2HolePosXY] )
                translate( [posXY[0], posXY[1], caseTopBorderOffset] )
                    translate( [0, 0, caseTopBorder/2 + manifoldCorrection] )
                        cube( [buttonHoleDimensions[0], buttonHoleDimensions[1], caseTopBorder + manifoldCorrection * 2], center = true );
        
            // button holes reset
            translate( [buttonResetHolePosXY[0], buttonResetHolePosXY[1], caseTopBorderOffset] )
                translate( [0, 0, caseTopBorder/2 + manifoldCorrection] )
                    rotate( [0, 0, 90] )
                        cube( [buttonHoleDimensions[0], buttonHoleDimensions[1], caseTopBorder + manifoldCorrection * 2], center = true ); 
        
            // PCB Post Bolt Holes
            for ( posXY = pcbMountingLocationsXY )
            {
                translate( [posXY[0], posXY[1], 0] )
                    boltNut(pcbBoltHeight, boltHeadDiameter, boltDiameter, boltHeadHeight, nutDiameter, pcbPostNutRecess);
            }            
        }
        
        // Case Post Bolt Holes
        for ( posXY = casePostsXY )
        {
            translate( [posXY[0], posXY[1], 0] )
                boltNut(caseBoltHeight, boltHeadDiameter, boltDiameter, boltHeadHeight, nutDiameter, casePostNutRecess);
        }
        
        // Vent Holes
        ventHolesInRectangle(ventsDiameter, ventsDistance, ventsXYMin[0], ventsXYMin[1], ventsXYMax[0], ventsXYMax[1], caseBottomBorder);

        // Potentiometer Hole
        translate( [potHoleXY[0], potHoleXY[1], caseOuterDimensions[2]-caseTopBorder-manifoldCorrection] )
            cylinder(d = potHoleDiameter, h = caseTopBorder + manifoldCorrection * 2);
            
        // GPS Hole
        translate( [-caseOuterDimensions[0]/2 - manifoldCorrection, gpsHoleOffsetY, gpsHoleOffsetZ] )
            rotate( [0, 90, 0] )
                cylinder(d = gpsHoleDiameter, h = caseSideBorder + manifoldCorrection * 2);
                
        // Wire Hole
        translate( [caseOuterDimensions[0]/2 - caseSideBorder/2, wireHoleY, caseSplitHeight - wireHoleDepth/2] )            
            cube( [caseSideBorder + manifoldCorrection * 2, wireHoleLength, wireHoleDepth + manifoldCorrection], center = true);
    }
}



module ventHolesInRectangle(diameter, distance, minX, minY, maxX, maxY, thickness, fn=6)
{
    translate( [0, 0, -manifoldCorrection] )
        for ( x = [minX:distance:maxX] )
            for ( y = [minY:distance:maxY] )
                translate( [x, y, 0] )
                    cylinder(d=diameter, h = thickness + manifoldCorrection * 2, $fn = fn);
}



module boltNut(totalLength, headDiameter, diameter, headHeight, nutDiameter, nutRecess)
{
    translate( [0, 0, -manifoldCorrection] )
    {
        cylinder(d = diameter, h = totalLength + 2 * manifoldCorrection);
        cylinder(d = nutDiameter, h = nutRecess + manifoldCorrection, $fn = 6);
        translate( [0, 0, totalLength - headHeight] )
            cylinder(d2 = headDiameter, d1 = diameter, h = headHeight + manifoldCorrection * 2);
    }
}



module postsPCBBottom()
{   
    translate( [0, 0, caseBottomBorder] )
    {
        // PCB Posts
        translate( [0, adafruitOffsetY, 0] )
            for ( posXY = pcbMountingLocationsXY )
            {
                translate( [posXY[0], posXY[1], 0] )
                {
                    donut(pcbPostReinforceDiameter, boltDiameter, pcbPostReinforceHeight);
                    donut(pcbPostBottomDiameter, boltDiameter, pcbBaseHeight );
                } 
            }        
    }

    // Case Posts
    for ( posXY = casePostsXY )
    {
        translate( [posXY[0], posXY[1], 0] )
        {
            donut(casePostReinforceDiameter, boltDiameter, casePostReinforceHeight);
            donut(casePostBottomDiameter, boltDiameter, caseBoltHeight );
        }   
    }
}



module postsPCBTop()
{   
    translate( [0, 0, caseBottomBorder] )
    {
        for ( posXY = pcbMountingLocationsXY )
        {
            translate( [posXY[0], posXY[1], caseInnerDimensions[2] - pcbTopPostHeight] )
                cylinder(d=pcbPostTopDiameter, h=pcbTopPostHeight); 
        }
    }
}



module roundedCube(dimensions, radius)
{
    xCenter = dimensions[0] / 2 - radius;
    yCenter = dimensions[1] / 2 - radius;
    
    hull()
    {
        for (pos = [[-xCenter, -yCenter], [xCenter, -yCenter], [-xCenter, yCenter], [xCenter, yCenter]])
        {
            translate( [pos[0], pos[1], 0] )
                cylinder( r = radius, h = dimensions[2] );
        }
    }
}



module lozenge(width, height, thickness)
{
    origin = (width - height)/2;
    
    hull()
    {
        translate( [-origin, 0, 0] )
            cylinder(d = height, h = thickness);

        translate( [origin, 0, 0] )
            cylinder(d = height, h = thickness);
    }
}



module donut(outerDiameter, innerDiameter, height)
{
    difference()
    {
        cylinder(d = outerDiameter, h = height);
        translate( [0, 0, -manifoldCorrection] )
            cylinder(d = innerDiameter, h = height + manifoldCorrection * 2);
    }
}