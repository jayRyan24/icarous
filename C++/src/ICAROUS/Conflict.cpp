/**
 * Conflict
 *
 * Conflict class
 *
 * Contact: Swee Balachandran (swee.balachandran@nianet.org)
 *
 *
 * Copyright (c) 2011-2016 United States Government as represented by
 * the National Aeronautics and Space Administration.  No copyright
 * is claimed in the United States under Title 17, U.S.Code. All Other
 * Rights Reserved.
 *
 * Notices:
 *  Copyright 2016 United States Government as represented by the Administrator of the National Aeronautics and Space Administration.
 *  All rights reserved.
 *
 * Disclaimers:
 *  No Warranty: THE SUBJECT SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND, EITHER EXPRESSED,
 *  IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
 *  IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR FREEDOM FROM INFRINGEMENT,
 *  ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL BE ERROR FREE, OR ANY WARRANTY THAT DOCUMENTATION, IF PROVIDED,
 *  WILL CONFORM TO THE SUBJECT SOFTWARE. THIS AGREEMENT DOES NOT, IN ANY MANNER, CONSTITUTE AN ENDORSEMENT BY GOVERNMENT
 *  AGENCY OR ANY PRIOR RECIPIENT OF ANY RESULTS, RESULTING DESIGNS, HARDWARE, SOFTWARE PRODUCTS OR ANY OTHER APPLICATIONS
 *  RESULTING FROM USE OF THE SUBJECT SOFTWARE.  FURTHER, GOVERNMENT AGENCY DISCLAIMS ALL WARRANTIES AND
 *  LIABILITIES REGARDING THIRD-PARTY SOFTWARE, IF PRESENT IN THE ORIGINAL SOFTWARE, AND DISTRIBUTES IT "AS IS."
 *
 * Waiver and Indemnity:
 *   RECIPIENT AGREES TO WAIVE ANY AND ALL CLAIMS AGAINST THE UNITED STATES GOVERNMENT,
 *   ITS CONTRACTORS AND SUBCONTRACTORS, AS WELL AS ANY PRIOR RECIPIENT.  IF RECIPIENT'S USE OF THE SUBJECT SOFTWARE
 *   RESULTS IN ANY LIABILITIES, DEMANDS, DAMAGES,
 *   EXPENSES OR LOSSES ARISING FROM SUCH USE, INCLUDING ANY DAMAGES FROM PRODUCTS BASED ON, OR RESULTING FROM,
 *   RECIPIENT'S USE OF THE SUBJECT SOFTWARE, RECIPIENT SHALL INDEMNIFY AND HOLD HARMLESS THE UNITED STATES GOVERNMENT,
 *   ITS CONTRACTORS AND SUBCONTRACTORS, AS WELL AS ANY PRIOR RECIPIENT, TO THE EXTENT PERMITTED BY LAW.
 *   RECIPIENT'S SOLE REMEDY FOR ANY SUCH MATTER SHALL BE THE IMMEDIATE, UNILATERAL TERMINATION OF THIS AGREEMENT.
 */
#include "Geofence.h"
#include "Conflict.h"

Conflict_t::Conflict_t(){
	keepin   = false;
	keepout  = false;
	flightPlanDeviation = false;
}

bool Conflict_t::isEqual(Geofence_t gf){

	if(gf.GetType() == KEEP_IN){
		for(itGeofence = keepInGeofence.begin();
			itGeofence != keepInGeofence.end();++itGeofence){
			if(gf.GetID() == itGeofence->GetID()){
				return true;
			}
		}
	}
	else{
		for(itGeofence = keepOutGeofence.begin();
			itGeofence != keepOutGeofence.end();++itGeofence){
			if(gf.GetID() == itGeofence->GetID()){
				return true;
			}
		}
	}
	return false;
}

void Conflict_t::AddConflict(Geofence_t gf){
	if(!isEqual(gf)){
		if(gf.GetType() == KEEP_IN){
			keepInGeofence.push_back(gf);
			printf("Keep in conflict\n");
		}
		else{
			keepOutGeofence.push_back(gf);
		}
	}
}

void Conflict_t::RemoveConflict(Geofence_t gf){
	if(gf.GetType() == KEEP_IN){
		for(itGeofence = keepInGeofence.begin();
			itGeofence != keepInGeofence.end();++itGeofence){
			if(gf.GetID() == itGeofence->GetID()){
				itGeofence = keepInGeofence.erase(itGeofence);
			}
		}
	}
	else{
		for(itGeofence = keepOutGeofence.begin();
			itGeofence != keepOutGeofence.end();++itGeofence){
			if(gf.GetID() == itGeofence->GetID()){
				itGeofence = keepOutGeofence.erase(itGeofence);
			}
		}
	}
}

uint8_t Conflict_t::size(){
	return keepInGeofence.size()+
			keepOutGeofence.size()+(int)flightPlanDeviation;
}

Geofence_t Conflict_t::GetKeepInConflict(){
	itGeofence = keepInGeofence.begin();
	return *itGeofence;
}

void Conflict_t::clear(){
	keepInGeofence.clear();
	keepOutGeofence.clear();
}
