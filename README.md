# Pipeline Inspector

Pipeline Inspector is a professional pre-delivery inspection tool for Blender, designed to help 3D artists ensure their assets are "Ready for Delivery" by automatically identifying technical issues before export, upload, or client submission.

## Project Vision

Pipeline Inspector is not just another mesh checker or geometry validator. It is a **Pre-Delivery Inspector**, functioning as a CI/CD-like validation gate for the 3D pipeline. Its goal is to help Blender users catch common errors—such as non-manifold geometry, flipped normals, missing textures, and unapplied transforms—before they cause project rework or client rejection.

## Key Features (MVP)

*   **Geometry Validation**: Detect non-manifold edges, N-gons, flipped normals, and loose geometry.
*   **UV & Texture Check**: Identify missing UVs, overlapping UVs, missing textures, and broken file paths.
*   **Transform Reset**: Verify that scale and rotation are applied and origins are correctly placed.
*   **Delivery Standards**: Check naming conventions and collection organization.
*   **Scoring System**: Provides a "READY FOR DELIVERY" score (0-100%) with a clear breakdown of Blocking Issues and Warnings.

## Project Structure

This repository contains the research, requirements, roadmap, and architecture documentation for the Pipeline Inspector project:

*   **/research**: Comprehensive market research, competitor analysis, and pain point rankings.
*   **/prd**: Product Requirements Document (PRD) and MVP definition.
*   **/roadmap**: Development roadmap for V1, V2, and V3.
*   **/architecture**: System architecture, module structure, and data flow design.

## Market Verdict

Based on our extensive research across communities like Blender Artists, Reddit, and Polycount, there is a **strong and genuine demand** for an integrated pre-delivery inspection tool in the Blender ecosystem. Existing tools are fragmented and often fail to provide a holistic "delivery readiness" assessment.

**Demand Score: 8/10**

## Status

The project is currently in the **Planning & Architecture** phase. Direct implementation has not yet begun, as we are prioritizing a "Research First" initiative to validate the core value proposition.

## License

[MIT License](LICENSE)
