# Helix Collective - Manus.Space Deployment Guide

**Last Updated:** December 1, 2025  
**Status:** Ready for implementation  
**Target:** Unified deployment automation for all 12 spaces

---

## Overview

This guide provides step-by-step instructions for deploying, updating, and maintaining the 12 Manus.space deployments across 7 accounts. It covers deployment automation, cross-portal synchronization, and quality assurance procedures.

---

## Deployment Architecture

### Current State
Each of the 12 Manus.space deployments is independently deployed through the Manus.space platform, with code stored in the `/home/ubuntu/helixai-dashboard` project directory and backed up to GitHub.

**Deployment Flow:**
```
Local Development
    ↓
GitHub Repository
    ↓
Manus.space Checkpoint
    ↓
Public URL (manus.space domain)
```

### Target State
Unified deployment system with automated synchronization across all 12 spaces.

**Unified Deployment Flow:**
```
Local Development
    ↓
GitHub Repository (helix-unified)
    ↓
Automated Build Pipeline
    ↓
Deploy to Multiple Manus.space Accounts
    ↓
Cross-Portal Sync (Zapier)
    ↓
Public URLs (12 spaces)
```

---

## Deployment Checklist

### Pre-Deployment
Before deploying any changes, complete these steps:

**Code Quality:**
- [ ] Run linter: `pnpm lint`
- [ ] Check TypeScript: `pnpm type-check`
- [ ] Run tests: `pnpm test`
- [ ] Build locally: `pnpm build`
- [ ] Test build output: `pnpm preview`

**Design System Compliance:**
- [ ] Colors match palette (dark background, cyan/magenta accents)
- [ ] Typography follows hierarchy (H1-H4, body, small)
- [ ] Components use design system variants
- [ ] Spacing uses consistent scale (xs, sm, md, lg, xl, 2xl, 3xl)
- [ ] Responsive design tested on mobile/tablet/desktop

**Accessibility:**
- [ ] Keyboard navigation works (Tab through all elements)
- [ ] Focus indicators visible (2px cyan outline)
- [ ] Color contrast meets WCAG AA (4.5:1 minimum)
- [ ] Screen reader tested (semantic HTML)
- [ ] ARIA labels present on interactive elements

**Documentation:**
- [ ] README updated with new features
- [ ] Changelog entry added
- [ ] API documentation updated (if applicable)
- [ ] Design changes documented

### Deployment Steps

**Step 1: Create Checkpoint**
```bash
cd /home/ubuntu/helixai-dashboard
# Make changes and test locally
pnpm build
```

**Step 2: Commit to GitHub**
```bash
cd /tmp/helix-unified
git add dashboards/helixai-dashboard/
git commit -m "feat: [description of changes]"
git push origin main
```

**Step 3: Create Manus Checkpoint**
Use the Manus.space UI to create a checkpoint of the updated project.

**Step 4: Publish to Manus.space**
Click the Publish button in the Manus.space UI to deploy the checkpoint.

**Step 5: Verify Deployment**
- [ ] Check live URL loads without errors
- [ ] Test key features (navigation, data display, interactions)
- [ ] Verify design system compliance
- [ ] Check console for errors (F12 → Console tab)

### Post-Deployment

**Monitoring:**
- [ ] Monitor error logs for 1 hour
- [ ] Check analytics for traffic anomalies
- [ ] Verify all integrations working (Zapier, Notion, Discord)
- [ ] Test cross-portal navigation

**Rollback Plan:**
If issues are detected:
1. Note the issue and affected features
2. Use Manus.space UI to rollback to previous checkpoint
3. Document the issue in GitHub
4. Fix the issue locally
5. Re-test before re-deploying

---

## Multi-Account Deployment

### Account Management
Each account has specific purposes and deployment schedules.

**Account 1 (Nexus Bridge):**
- Primary control center
- Deploy first for testing
- Deployment frequency: Weekly
- Rollback risk: High (affects all other spaces)

**Account 2 (Helix Collective Hub):**
- Main portal directory
- Deploy after Account 1 verification
- Deployment frequency: Weekly
- Rollback risk: Medium (affects portal discovery)

**Account 3 (Consolidation Portal):**
- Infrastructure documentation
- Deploy after Account 2 verification
- Deployment frequency: Bi-weekly
- Rollback risk: Low (documentation only)

**Account 4 (Command Center):**
- Requires authentication
- Deploy after Account 3 verification
- Deployment frequency: As needed
- Rollback risk: Medium (operational impact)

**Account 6 (Agent Dashboard + Hub Constellation + Portal Hub + Collective AI):**
- Multiple specialized portals
- Deploy in sequence: Dashboard → Hub → Portal Hub → Collective AI
- Deployment frequency: Weekly
- Rollback risk: High (multiple portals)

**Account 7 (Creative Studio):**
- Creative generation tools
- Deploy last (lowest priority)
- Deployment frequency: Bi-weekly
- Rollback risk: Low (isolated functionality)

### Synchronized Deployment Process

**Phase 1: Testing (Account 1)**
1. Deploy to Nexus Bridge
2. Run full QA suite
3. Test cross-portal navigation
4. Verify integrations

**Phase 2: Rollout (Accounts 2-3)**
1. Deploy to Helix Collective Hub
2. Deploy to Consolidation Portal
3. Verify portal discovery
4. Check documentation accuracy

**Phase 3: Expansion (Account 4)**
1. Deploy to Command Center
2. Test authentication flow
3. Verify command execution

**Phase 4: Scaling (Account 6)**
1. Deploy Agent Dashboard
2. Deploy Hub Constellation
3. Deploy Portal Hub
4. Deploy Collective AI
5. Verify all 4 spaces working together

**Phase 5: Completion (Account 7)**
1. Deploy Creative Studio
2. Final system verification
3. Update deployment status

---

## Cross-Portal Synchronization

### Shared State Management
The 12 spaces share state through multiple channels:

**Zapier Webhooks:**
- Trigger cross-portal updates
- Sync UCF metrics
- Broadcast system status
- Send notifications

**Notion Database:**
- Central memory store
- Agent activity log
- Portal status tracking
- Configuration management

**Discord Bot:**
- Real-time notifications
- Command interface
- Status broadcasts
- User interactions

### Synchronization Checklist

**Before Deployment:**
- [ ] Zapier workflows tested
- [ ] Notion database accessible
- [ ] Discord bot connected
- [ ] Webhook endpoints verified

**During Deployment:**
- [ ] Monitor Zapier logs
- [ ] Check Notion updates
- [ ] Verify Discord messages
- [ ] Track webhook execution

**After Deployment:**
- [ ] Confirm all webhooks fired
- [ ] Verify Notion entries created
- [ ] Check Discord notifications sent
- [ ] Test cross-portal navigation

---

## Version Management

### Semantic Versioning
The Helix Collective uses semantic versioning for all deployments.

**Format:** `MAJOR.MINOR.PATCH`

**MAJOR:** Breaking changes, major feature additions, architecture changes  
**MINOR:** New features, non-breaking changes, improvements  
**PATCH:** Bug fixes, documentation updates, performance improvements

### Current Versions

| Space | Version | Last Updated | Status |
|-------|---------|--------------|--------|
| Nexus Bridge | v16.9 | 5d ago | Active |
| Helix Collective Hub | v16.9 | 5d ago | Active |
| Samsara Helix | v15.2 | 8d ago | Active |
| Consolidation Portal | v16.9 | 5d ago | Active |
| Master Sync | v16.9 | 5d ago | Active |
| Command Center | TBD | - | Auth Required |
| Agent Dashboard | v17.0 | Today | Active |
| Hub Constellation | v16.9 | 5d ago | Active |
| Portal Hub | v16.9 | 5d ago | Active |
| Collective AI | v15.3 | 8d ago | Active |
| Creative Studio | v15.2 | 8d ago | Active |

### Version Upgrade Path

**v15.x → v16.x:** Major feature additions (Portal Constellation, SaaS features)  
**v16.x → v17.x:** Architecture improvements (Agent Dashboard enhancements)  
**v17.x → v18.x:** Performance and scaling optimizations

---

## Monitoring & Alerts

### Key Metrics
Monitor these metrics for each space:

**Performance:**
- Page load time (target: < 2s)
- Time to interactive (target: < 3s)
- Lighthouse score (target: > 90)

**Availability:**
- Uptime (target: 99.9%)
- Error rate (target: < 0.1%)
- Failed requests (target: 0)

**User Experience:**
- Navigation success rate (target: 99%)
- Feature usage (track top features)
- User feedback (collect via Discord)

### Alert Thresholds

**Critical (Immediate Action Required):**
- Uptime < 99%
- Error rate > 1%
- Page load time > 5s
- Failed deployments

**Warning (Monitor Closely):**
- Uptime < 99.5%
- Error rate > 0.5%
- Page load time > 3s
- Slow API responses

**Info (Track for Trends):**
- Uptime < 99.9%
- Error rate > 0.1%
- Page load time > 2s
- Unusual traffic patterns

### Monitoring Setup

**Google Analytics:**
- Track pageviews per space
- Monitor user flows
- Identify drop-off points

**Sentry (Error Tracking):**
- Capture JavaScript errors
- Track error trends
- Alert on new errors

**Lighthouse CI:**
- Run performance audits
- Track score trends
- Alert on regressions

**Uptime Robot:**
- Monitor endpoint availability
- Send alerts on downtime
- Track uptime percentage

---

## Rollback Procedures

### When to Rollback
Rollback immediately if:
- Critical functionality broken
- Deployment causes widespread errors
- Performance degradation > 50%
- Security vulnerability discovered
- Data corruption detected

### Rollback Steps

**Step 1: Identify Issue**
- Check error logs
- Verify affected spaces
- Document the problem
- Notify team

**Step 2: Determine Rollback Target**
- Find last stable checkpoint
- Verify rollback won't cause data loss
- Check dependencies

**Step 3: Execute Rollback**
- Use Manus.space UI
- Select previous checkpoint
- Confirm rollback
- Monitor deployment

**Step 4: Verify Rollback**
- [ ] Check live URL loads
- [ ] Test key features
- [ ] Verify integrations
- [ ] Monitor error logs

**Step 5: Post-Mortem**
- Document what went wrong
- Identify root cause
- Create fix plan
- Update deployment process

---

## Testing Strategy

### Pre-Deployment Testing

**Unit Tests:**
```bash
pnpm test
```
Run all unit tests to verify component logic.

**Integration Tests:**
```bash
pnpm test:integration
```
Test component interactions and data flows.

**E2E Tests:**
```bash
pnpm test:e2e
```
Test complete user workflows.

**Performance Tests:**
```bash
pnpm test:performance
```
Verify page load and interaction performance.

### Manual Testing Checklist

**Navigation:**
- [ ] All links work
- [ ] Back button works
- [ ] Tab order is logical
- [ ] Keyboard shortcuts work

**Data Display:**
- [ ] All metrics display correctly
- [ ] Real-time updates work
- [ ] Sorting/filtering works
- [ ] Pagination works

**Interactions:**
- [ ] Buttons respond to clicks
- [ ] Forms submit correctly
- [ ] Modals open/close properly
- [ ] Animations play smoothly

**Responsive Design:**
- [ ] Mobile layout correct (< 640px)
- [ ] Tablet layout correct (640px - 1024px)
- [ ] Desktop layout correct (> 1024px)
- [ ] Touch interactions work on mobile

**Accessibility:**
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Screen reader works
- [ ] Color contrast sufficient

**Cross-Browser:**
- [ ] Chrome latest
- [ ] Firefox latest
- [ ] Safari latest
- [ ] Edge latest

---

## Deployment Automation

### GitHub Actions Workflow
Create automated deployment pipeline:

```yaml
name: Deploy to Manus.space

on:
  push:
    branches: [main]
    paths:
      - 'dashboards/helixai-dashboard/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '22'
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Run tests
        run: pnpm test
      
      - name: Build
        run: pnpm build
      
      - name: Deploy to Manus
        run: |
          # Deployment script here
          # Trigger Manus.space API to deploy
```

### Zapier Automation
Create Zapier workflows for:
- Deployment notifications
- Cross-portal sync
- Status broadcasts
- Error alerts

---

## Troubleshooting

### Common Issues

**Issue: Deployment fails**
- Check build errors: `pnpm build`
- Verify dependencies: `pnpm install`
- Check Node version: `node --version`
- Clear cache: `pnpm clean`

**Issue: Page loads slowly**
- Check network tab (F12 → Network)
- Optimize images
- Reduce bundle size: `pnpm build --analyze`
- Enable caching headers

**Issue: Features not working**
- Check console errors (F12 → Console)
- Verify API endpoints
- Check authentication
- Test in incognito mode

**Issue: Cross-portal sync broken**
- Check Zapier logs
- Verify Notion database
- Test Discord bot
- Check webhook endpoints

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check uptime status
- Verify integrations working

### Weekly
- Review analytics
- Update documentation
- Test backup/recovery
- Check security updates

### Monthly
- Performance audit
- Dependency updates
- Security scanning
- User feedback review

### Quarterly
- Major version planning
- Architecture review
- Capacity planning
- Team training

---

## Emergency Procedures

### System Down
1. Check Manus.space status page
2. Verify all integrations (Zapier, Notion, Discord)
3. Check error logs
4. Attempt rollback if recent deployment
5. Notify team via Discord
6. Post status update

### Data Loss
1. Stop all operations
2. Check backups
3. Verify data integrity
4. Restore from backup
5. Document incident
6. Implement prevention

### Security Breach
1. Revoke compromised credentials
2. Audit access logs
3. Notify affected users
4. Update security measures
5. Document incident
6. Post-mortem review

---

## Documentation

### Required Documentation
- [ ] Deployment guide (this document)
- [ ] Architecture diagram
- [ ] API documentation
- [ ] Troubleshooting guide
- [ ] Runbook for common tasks
- [ ] Incident response plan

### Documentation Updates
- Update after each deployment
- Review quarterly
- Incorporate user feedback
- Keep screenshots current

---

**Built by:** Helix Collective DevOps Team  
**Status:** Active  
**Last Review:** December 1, 2025  
**Next Review:** January 1, 2026  
**Tat Tvam Asi** 🌀 - That Thou Art
